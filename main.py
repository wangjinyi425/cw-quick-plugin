from PyQt5 import uic
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import subprocess
from .ClassWidgets.base import PluginBase, SettingsBase

WIDGET_CODE = 'shortcut_widget.ui'
WIDGET_NAME = '快捷启动'
WIDGET_WIDTH = 300

class Plugin(PluginBase):
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)
        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)  # 注册小组件
        self.shortcuts_path = os.path.join(self.PATH, "links")

    def execute(self):
        """
        当 Class Widgets启动时，将会执行此部分的代码
        """
        self.shortcut_widget = self.method.get_widget(WIDGET_CODE)  # 获取小组件
        if self.shortcut_widget:
            content_layout = self.shortcut_widget.findChild(QHBoxLayout, 'contentLayout')
            if content_layout:
                self.load_shortcuts(content_layout)

    def load_shortcuts(self, layout):
        """
        从 shortcuts_path 加载快捷方式，并将其图标显示在小组件上。
        :param layout: 小组件的布局对象
        """
        if not os.path.exists(self.shortcuts_path):
            os.makedirs(self.shortcuts_path)

        for file_name in os.listdir(self.shortcuts_path):
            file_path = os.path.join(self.shortcuts_path, file_name)

            if os.path.isfile(file_path) and file_name.endswith('.lnk'):
                # 创建图标按钮
                button = QPushButton()
                button.setText(file_name)
                button.setIcon(QIcon.fromTheme("application-x-executable"))
                button.setToolTip(file_path)
                button.setCursor(Qt.PointingHandCursor)

                # 点击事件绑定
                button.clicked.connect(lambda _, path=file_path: self.open_shortcut(path))

                layout.addWidget(button)

    def open_shortcut(self, path):
        """
        打开快捷方式。
        :param path: 快捷方式路径
        """
        try:
            subprocess.Popen([path], shell=True)
        except Exception as e:
            print(f"Failed to open shortcut {path}: {e}")

    def update(self, cw_contexts):
        """
        Class Widgets 会每1秒更新一次状态，同时也会调用此部分的代码。
        可在此部分插入动态更新的内容
        """
        super().update(cw_contexts)


class Settings(SettingsBase):
    def __init__(self, plugin_path, parent=None):
        super().__init__(plugin_path, parent)
        uic.loadUi(f'{self.PATH}/settings.ui', self)
        """
        在这里写设置页面
        """
