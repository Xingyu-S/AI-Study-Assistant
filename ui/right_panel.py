import markdown
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QCheckBox, QMenu, QFileDialog)
from PyQt6.QtCore import pyqtSignal, QUrl
# 【修正1】引入 QColor
from PyQt6.QtGui import QColor 
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings

class RightPanel(QWidget):
    send_message_signal = pyqtSignal(str, bool)   
    change_folder_signal = pyqtSignal()
    cleanup_light_signal = pyqtSignal()
    cleanup_deep_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # === 1. 顶部按钮区 ===
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(5, 5, 5, 5)
        
        self.change_btn = QPushButton("📂 切换项目")
        self.change_btn.clicked.connect(self.change_folder_signal.emit)
        
        self.cleanup_btn = QPushButton("🧹 清理")
        self.cleanup_menu = QMenu()
        action_light = self.cleanup_menu.addAction("🍃 轻度清理 (仅清理缓存)")
        action_light.triggered.connect(self.cleanup_light_signal.emit)
        action_deep = self.cleanup_menu.addAction("🔥 深度清理 (删除历史记录)")
        action_deep.triggered.connect(self.cleanup_deep_signal.emit)
        self.cleanup_btn.setMenu(self.cleanup_menu)

        btn_layout.addWidget(self.change_btn)
        btn_layout.addWidget(self.cleanup_btn)
        btn_layout.addStretch() 

        # === 2. 聊天显示区 (升级为浏览器内核) ===
        self.chat_view = QWebEngineView()
        
        # 【修正2】使用 QColor 转换颜色字符串
        bg_color_str = os.environ.get("QT_BACKGROUND_COLOR", "#ffffff")
        self.chat_view.page().setBackgroundColor(QColor(bg_color_str))
        
        # 内部存储消息历史
        self.history_messages = [] 

        # === 3. 底部输入区 ===
        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(5, 5, 5, 5)
        
        self.screen_check = QCheckBox("📷 读取屏幕")
        self.screen_check.setChecked(True) 
        self.screen_check.setToolTip("勾选后，AI 将能看到你当前的浏览器画面")

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("输入问题...")
        self.chat_input.returnPressed.connect(self._on_send_click)
        
        self.send_btn = QPushButton("发送")
        self.send_btn.clicked.connect(self._on_send_click)
        
        input_layout.addWidget(self.screen_check) 
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(btn_layout)
        layout.addWidget(self.chat_view, stretch=1) 
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
        self.render_chat()

    def _on_send_click(self):
        text = self.chat_input.text().strip()
        if text:
            need_screenshot = self.screen_check.isChecked()
            self.send_message_signal.emit(text, need_screenshot)
            self.chat_input.clear()

    def append_message(self, role, text):
        """添加一条消息并刷新显示"""
        self.history_messages.append({"role": role, "text": text})
        self.render_chat()

    def clear_history(self):
        """清空聊天记录"""
        self.history_messages = []
        self.render_chat()

    def render_chat(self):
        """将所有消息转换为带有 MathJax 和 CSS 的 HTML"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body { font-family: 'Segoe UI', sans-serif; padding: 10px; background-color: #f9f9f9; }
                
                /* 消息气泡样式 */
                .message { margin-bottom: 15px; padding: 10px 15px; border-radius: 10px; line-height: 1.6; max-width: 90%; }
                .user { background-color: #e3f2fd; margin-left: auto; color: #0d47a1; border-bottom-right-radius: 2px; }
                .model { background-color: #ffffff; margin-right: auto; color: #333; border: 1px solid #ddd; border-bottom-left-radius: 2px; }
                
                /* 角色标签 */
                .role-label { font-size: 12px; font-weight: bold; margin-bottom: 5px; color: #666; }
                
                /* Markdown 元素样式 */
                p { margin: 5px 0; }
                code { background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; font-family: Consolas, monospace; color: #d63384; }
                pre { background-color: #2b2b2b; color: #f8f8f2; padding: 10px; border-radius: 5px; overflow-x: auto; }
                pre code { background-color: transparent; color: inherit; }
                
                /* 表格样式 */
                table { border-collapse: collapse; width: 100%; margin: 10px 0; background-color: white; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; font-weight: bold; }
                tr:nth-child(even) { background-color: #fafafa; }

                /* 引用样式 */
                blockquote { border-left: 4px solid #ccc; margin: 0; padding-left: 10px; color: #666; }
            </style>
            
            <script>
            window.MathJax = {
              tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
              }
            };
            </script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        </head>
        <body>
        """

        for msg in self.history_messages:
            role_name = "我" if msg['role'] == "user" else "AI 助手"
            css_class = "user" if msg['role'] == "user" else "model"
            
            try:
                content_html = markdown.markdown(
                    msg['text'], 
                    extensions=['tables', 'fenced_code', 'nl2br']
                )
            except:
                content_html = msg['text']

            html_content += f"""
            <div class='role-label' style='text-align: {"right" if msg['role'] == "user" else "left"};'>
                {role_name}
            </div>
            <div class='message {css_class}'>
                {content_html}
            </div>
            <div style="clear: both;"></div>
            """

        html_content += """
        <script>
            window.scrollTo(0, document.body.scrollHeight);
        </script>
        </body>
        </html>
        """
        
        self.chat_view.setHtml(html_content)