import sys
from PyQt6.QtWidgets import QApplication
# 注意这里：是从 ui包 里的 main_window模块 导入 AIProjectWindow类
from ui.main_window import AIProjectWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIProjectWindow()
    window.show()
    sys.exit(app.exec())