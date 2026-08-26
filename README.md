# AI Study Assistant（AI 学习助手）

AI Study Assistant is a personal, AI-assisted desktop prototype for asking questions about learning materials that the user is authorised to access. It combines an embedded viewer, optional screen capture, the Google Gemini API, and a Markdown/MathJax response panel.

AI Study Assistant 是一个个人使用的 AI 辅助桌面原型，用于对用户有权访问的学习材料进行提问。它结合了内嵌浏览器、可选的屏幕截图、Google Gemini API，以及支持 Markdown/MathJax 的回答面板。

## Scope and responsible use（使用范围与合规边界）

This project is intended only for content that the user has lawfully obtained and is authorised to view and process. It does **not** provide access to protected content, remove DRM, bypass authentication, or grant permission to use third-party material. Users remain responsible for complying with applicable law, copyright, licence terms, and platform terms of service.

本项目仅用于用户合法获得、并有权查看和处理的内容。它**不**提供对受保护内容的访问权限，不移除 DRM，不绕过身份验证，也不代表用户已获得处理第三方材料的许可。使用者应自行遵守适用法律、版权、许可条件及平台服务条款。

The embedded browser currently uses a fixed compatibility user-agent string and a persistent local browser profile. These settings are for application compatibility and session continuity, not for bypassing access controls.

内嵌浏览器目前使用固定的兼容性 User-Agent，并保存本地浏览器配置，以改善兼容性和会话连续性；这些设置并非用于绕过访问控制。

## What it does（主要功能）

### 1. Embedded viewing（内嵌阅读）

- Opens web pages in an embedded PyQt6 WebEngine view.
- Opens local PDF files supported by the embedded viewer.
- Retains a local browser profile so that ordinary session data can persist between launches.

### 2. Optional visual Q&A（可选的视觉问答）

- When **Read Screen** is enabled, the application captures the currently displayed viewer area and sends the image to the Gemini API with the user's question.
- The user-written prompt asks the model to focus on the main learning content and ignore interface elements such as menus, buttons, and sidebars.
- This approach was selected after direct extraction from browser content proved unreliable during prototyping.

### 3. Rendered responses（格式化回答）

- Displays Markdown, tables, code blocks, and mathematical notation through a web-based response panel.
- Uses MathJax for mathematical rendering.
- Model responses may still contain factual, formatting, or interpretation errors and should be checked by the user.

### 4. Bilingual study notes（双语学习笔记）

- The prompt requests a Chinese explanation of the selected material.
- It also requests a short bilingual list of key terms or phrases for review.

### 5. Local continuity controls（本地连续性功能）

- Remembers the last selected project folder and URL.
- Stores local conversation history for later sessions.
- Provides light and deep cleanup options for browser data and AI conversation context.

### 6. Folder-context mode（文件夹上下文模式）

- When **Read Screen** is disabled, the application can collect readable text/code files from a user-selected folder and send that context with a question.
- Only select folders and files that you are authorised to send to the Gemini API. Do not use this mode for secrets, credentials, personal data, or confidential material.

## Data handling and privacy（数据处理与隐私）

Depending on the selected mode, screenshots or selected-folder content are transmitted to the Google Gemini API for processing. Local browser data, configuration, and conversation history may also be stored on the device. Review Google's applicable API terms and privacy documentation before use.

根据所选模式，屏幕截图或所选文件夹中的内容会被发送至 Google Gemini API 处理。浏览器数据、配置和对话历史也可能保存在本地设备上。使用前请阅读 Google 适用的 API 条款和隐私说明。

The API key is read from a local `gemini_API.txt` file, which is excluded by `.gitignore`. Never commit or share this file.

## Quick start（快速开始）

### 1. Clone the repository

```bash
git clone https://github.com/Xingyu-S/AI-Study-Assistant.git
cd AI-Study-Assistant
```

### 2. Install dependencies

Python 3.8 or later is recommended.

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create `gemini_API.txt` in the repository root and place the API key in that file. Do not add quotation marks or commit the file.

### 4. Run the application

```bash
python main.py
```

## Technology used（技术构成）

- Python
- PyQt6 and PyQt6-WebEngine
- Google Gemini API
- Markdown, HTML/CSS, and MathJax

## Limitations（局限）

- This is a personal prototype, not a production application or a security-audited tool.
- The model can produce inaccurate or incomplete answers.
- Website compatibility, authentication, and embedded viewing may vary by provider.
- The project has not been presented as an independently programmed software-engineering project.

## Authorship and AI-use disclosure（作者分工与 AI 使用披露）

The author independently defined the product need, feature requirements, workflow, prompts, and testing and iteration decisions. The author also installed the dependencies, ran the application, identified bugs, and directed changes, including the move from direct browser-content extraction to a visual approach and the addition of last-URL/project-state restoration.

Google Gemini suggested using PyQt6 and the Gemini API and generated **all implementation code**. Gemini also generated the original README/project-description text. The author does not claim independent authorship of the code or present this repository as evidence of independent programming or software-engineering ability. This README was later revised with AI assistance to make the scope, limitations, and division of work explicit.

作者独立提出产品需求，决定功能、工作流、提示词及测试和迭代方向；并自行安装依赖、运行程序、识别问题和提出修改，包括从直接读取浏览器内容转向视觉方案，以及增加恢复上次 URL/项目状态的功能。

Google Gemini 建议采用 PyQt6 和 Gemini API，并生成了**全部实现代码**；原始 README/项目描述文本也由 Gemini 生成。作者不主张对代码的独立创作，也不将本仓库作为独立编程或软件工程能力的证明。本版 README 后续借助 AI 修订，以明确项目范围、局限和实际分工。
