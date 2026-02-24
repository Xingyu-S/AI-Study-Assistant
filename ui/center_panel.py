from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QFileDialog)
# 清理掉了不用的引用 (字体、颜色、Splitter等)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal, QBuffer, QIODevice
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
import base64
import os

# --- 浏览器类 ---
class MyBrowser(QWebEngineView):
    def createWindow(self, _type):
        return self

class CenterPanel(QWidget):
    # 移除了 note_changed_signal
    url_changed_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # === 1. 顶部导航栏 (保留) ===
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(5, 5, 5, 5)

        self.btn_back = QPushButton("←")
        self.btn_forward = QPushButton("→")
        self.btn_reload = QPushButton("↻")
        self.btn_back.setFixedSize(30, 30)
        self.btn_forward.setFixedSize(30, 30)
        self.btn_reload.setFixedSize(30, 30)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("输入网址 或 本地文件路径...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.btn_pdf = QPushButton("📄 打开PDF")
        self.btn_pdf.clicked.connect(self.open_local_pdf)

        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        nav_layout.addWidget(self.url_bar)
        nav_layout.addWidget(self.btn_pdf)

        # === 2. 浏览器区域 (独占全屏) ===
        self.browser = MyBrowser() 
        
        # 设置 (保留 PDF 支持和伪装)
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
        
        fake_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        profile = self.browser.page().profile()
        profile.setHttpUserAgent(fake_user_agent)
        profile.setPersistentStoragePath(os.path.join(os.getcwd(), ".browser_data"))
        
        self.browser.urlChanged.connect(self.update_url_bar)
        self.btn_back.clicked.connect(self.browser.back)
        self.btn_forward.clicked.connect(self.browser.forward)
        self.btn_reload.clicked.connect(self.browser.reload)

        # 直接把导航栏和浏览器加入主布局，不再需要 Splitter
        layout.addLayout(nav_layout)
        layout.addWidget(self.browser) 
        self.setLayout(layout)

    # --- 导航逻辑 (保留) ---
    def navigate_to_url(self):
        url_input = self.url_bar.text().strip()
        if not url_input: return
        self.load_url(url_input)

    def load_url(self, url_str):
        if not url_str: return
        if os.path.exists(url_str):
            self.browser.setUrl(QUrl.fromLocalFile(url_str))
            return
        if url_str.lower().startswith("http") or url_str.lower().startswith("file:"):
            self.browser.setUrl(QUrl(url_str))
            return
        self.browser.setUrl(QUrl("https://" + url_str))

    def update_url_bar(self, qurl):
        url_str = qurl.toString()
        if qurl.isLocalFile():
            self.url_bar.setText(qurl.toLocalFile())
        else:
            self.url_bar.setText(url_str)
        self.url_changed_signal.emit(url_str)

    def open_local_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if file_path:
            self.browser.setUrl(QUrl.fromLocalFile(file_path))

    # --- 截图功能 (AI 视觉核心，必须保留) ---
    def capture_screenshot(self):
        pixmap = self.browser.grab()
        buffer = QBuffer()
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buffer, "JPEG", quality=80)
        image_bytes = buffer.data().data()
        base64_str = base64.b64encode(image_bytes).decode('utf-8')
        return base64_str

    def clear_browser_cache(self):
        profile = self.browser.page().profile()
        profile.clearHttpCache()
        profile.clearAllVisitedLinks()
        cookie_store = profile.cookieStore()
        cookie_store.deleteAllCookies()