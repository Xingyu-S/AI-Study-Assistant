import os
import json 
from PyQt6.QtWidgets import QMainWindow, QSplitter, QMessageBox, QFileDialog, QApplication
from PyQt6.QtCore import Qt

from .left_panel import LeftPanel
from .center_panel import CenterPanel
from .right_panel import RightPanel
from core.manager import ProjectAssistant

class AIProjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的 AI 学习助手 (极简浏览版)")
        self.resize(1400, 900)

        self.assistant = ProjectAssistant()
        
        self.current_project_path = os.getcwd()
        self.load_global_config()

        self.left_panel = LeftPanel(self.current_project_path)
        self.center_panel = CenterPanel()
        self.right_panel = RightPanel()

        self.init_ui()
        self.connect_signals()
        
        self.load_initial_history()
        # 移除了 load_notes()
        self.load_last_url()

    def init_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.center_panel)
        splitter.addWidget(self.right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4) # 让中间浏览器区域更大
        splitter.setStretchFactor(2, 2)
        
        self.setCentralWidget(splitter)

    def connect_signals(self):
        self.left_panel.file_clicked_signal.connect(self.handle_file_click)
        self.right_panel.send_message_signal.connect(self.handle_send_message_click)
        self.right_panel.change_folder_signal.connect(self.handle_change_folder)
        # 移除了 note_changed_signal 的连接
        self.right_panel.cleanup_light_signal.connect(self.handle_light_cleanup)
        self.right_panel.cleanup_deep_signal.connect(self.handle_deep_cleanup)
        self.center_panel.url_changed_signal.connect(self.save_last_url)

    # --- 全局记忆逻辑 ---
    def load_global_config(self):
        try:
            with open("global_config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                saved_path = data.get("last_project_path")
                if saved_path and os.path.exists(saved_path):
                    self.current_project_path = saved_path
        except:
            pass

    def save_global_config(self):
        try:
            data = {"last_project_path": self.current_project_path}
            with open("global_config.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_last_url(self):
        config = self.assistant.history_manager.load_config(self.current_project_path)
        last_url = config.get("last_url", "https://www.bing.com")
        self.center_panel.load_url(last_url)

    def save_last_url(self, url):
        config = self.assistant.history_manager.load_config(self.current_project_path)
        config["last_url"] = url
        self.assistant.history_manager.save_config(self.current_project_path, config)

    def load_initial_history(self):
        self.right_panel.clear_history()
        history = self.assistant.load_history(self.current_project_path)
        if history:
            for msg in history:
                self.right_panel.append_message(msg['role'], msg['text'])

    # --- 移除了 load_notes, save_notes, get_note_path ---

    # --- 清理与交互 ---
    def handle_light_cleanup(self):
        self.center_panel.clear_browser_cache()
        QMessageBox.information(self, "完成", "已清理浏览器缓存和 Cookies。")

    def handle_deep_cleanup(self):
        reply = QMessageBox.question(self, "确认", 
                                   "确定要执行深度清理吗？\n这将删除历史记录。",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.center_panel.clear_browser_cache()
            self.assistant.clear_active_history(self.current_project_path)
            self.right_panel.clear_history()
            QMessageBox.information(self, "完成", "已重置 AI 记忆。")

    def handle_send_message_click(self, user_text, need_screenshot):
        self.right_panel.append_message("user", user_text)
        self.right_panel.chat_input.setDisabled(True) 
        
        if need_screenshot:
            self.right_panel.append_message("model", "<i>正在截取屏幕并识别...</i>")
            QApplication.processEvents() 
            screenshot_b64 = self.center_panel.capture_screenshot()
            self.send_to_ai(user_text, screenshot_b64)
        else:
            self.right_panel.append_message("model", "<i>思考中...</i>")
            QApplication.processEvents()
            self.send_to_ai(user_text, None)

    def send_to_ai(self, user_text, image_data):
        QApplication.processEvents()
        response = self.assistant.chat(user_text, self.current_project_path, image_data=image_data)
        self.right_panel.append_message("model", response)
        self.right_panel.chat_input.setDisabled(False)

    def handle_file_click(self, file_path):
        self.center_panel.load_url(file_path)

    def handle_change_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择学习项目文件夹")
        if folder:
            self.current_project_path = folder
            self.save_global_config()
            self.left_panel.update_project_path(folder)
            self.load_initial_history() 
            self.load_last_url()
            # 移除了 self.load_notes()