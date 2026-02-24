# 🎓 AI-Study-Assistant (AI 学习助手)

A desktop-based AI study assistant built with **Python (PyQt6)** and **Google Gemini 1.5 Flash Vision**. 
Specifically designed for reading foreign original textbooks, CIMA/ACCA e-books, and DRM-protected PDF materials.

*(基于 PyQt6 和 Gemini API 开发的桌面端专属 AI 学习外挂，专为阅读外文教材和受保护的 PDF 资料设计。)*

## 💡 Why built this? (开发初衷)

When studying on overseas textbook platforms like Kaplan or BibliU, students often face:
1. **DRM Restrictions**: Incapable of selecting or copying text for translation.
2. **Anti-bot Blocking**: Standard embedded browsers are often blocked with errors like "Browser is looking retro".
3. **Rendering Mess**: Traditional AI chat boxes fail to render complex financial tables and higher math formulas.

**This project perfectly solves these issues through a combination of "Vision LLM Screenshot QA" + "Disguised Browser" + "MathJax Frontend Rendering".**
## ✨ Key Features (核心功能)

### 👁️ 1. Vision AI Integration (突破限制的“视觉提问”)
- **Screenshot QA**: Check "Read Screen" (读取屏幕) to silently capture the current e-book page in high definition. The image is converted to Base64 and fed to the Gemini Vision model. The AI can "see" your book even if copying is disabled.
- **Anti-interference Prompt**: Exclusive System Prompts instruct the AI to ignore UI elements (sidebars, buttons) and focus solely on the main text.

### 🌐 2. Anti-blocking Browser (防拦截浏览器)
- **User-Agent Disguise**: A deeply customized QtWebEngine disguised as the latest Windows Chrome, easily bypassing strict textbook website gates.
- **Persistent Storage**: Auto-saves Cookies so you stay logged in.
- **Native PDF Support**: Drag and drop or load local high-res PDFs directly into the browser for Vision AI analysis.

### 🧮 3. Academic Chat Render (学术级对话渲染)
- **Dynamic HTML Core**: The right-side chat panel is rebuilt on a Web engine, abandoning plain text boxes.
- **Perfect Math & Tables**: Integrated with **MathJax** and Markdown Tables. Complex financial formulas (e.g., ROCE, Calculus) and multi-line tables are rendered flawlessly like a textbook.

### 📝 4. Auto Bilingual Notes (自动双语笔记)
- **Core Vocabulary Extraction**: After explaining the page content, the AI automatically summarizes 3-5 core professional terms, generating a 【Bilingual Core Note】 to boost cross-lingual study efficiency.

### 🧠 5. Global Memory (全局记忆)
- **Scene Restoration**: Automatically remembers your last exited project folder and URL. Double-click to instantly return to your study scene.
- **Cache Management**: Supports "Light Clean" (clear browser cache) and "Deep Clean" (reset AI context memory).
## 🛠️ Quick Start (快速开始)

**1. Prerequisites**
Ensure Python 3.8+ is installed. Clone this repository:
```bash
git clone [https://github.com/YourUsername/AI-Study-Assistant.git](https://github.com/YourUsername/AI-Study-Assistant.git)
cd AI-Study-Assistant
```

**2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure API Key**
Create a new file named `gemini_API.txt` in the root directory and paste your Google Gemini API Key in plain text. *(This file is ignored by `.gitignore` to prevent leakage).*

**4. Run the App**
```bash
python main.py
```

## ⚙️ Tech Stack (技术栈)
- **GUI Framework**: PyQt6, PyQt6-WebEngine
- **AI API**: Google Generative AI (Gemini 1.5 Flash API)
- **Frontend Render**: Markdown (Python), MathJax, HTML/CSS
