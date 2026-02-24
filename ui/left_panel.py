import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView
from PyQt6.QtCore import QDir, pyqtSignal
from PyQt6.QtGui import QFileSystemModel

class LeftPanel(QWidget):
    # 自定义信号：当文件被点击时，对外发送文件的路径字符串
    file_clicked_signal = pyqtSignal(str)

    def __init__(self, project_path):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0) # 去掉边距，更紧凑

        # 文件系统模型
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())

        # 树形视图
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.update_project_path(project_path)
        
        # 隐藏多余列
        for i in range(1, 4):
            self.file_tree.setColumnHidden(i, True)
        
        # 连接内部点击事件
        self.file_tree.clicked.connect(self._on_click)
        
        layout.addWidget(self.file_tree)
        self.setLayout(layout)

    def update_project_path(self, path):
        """外部调用此方法来切换文件夹"""
        self.file_tree.setRootIndex(self.file_model.index(path))

    def _on_click(self, index):
        """内部处理点击，转换成路径发送给主窗口"""
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path):
            self.file_clicked_signal.emit(file_path)