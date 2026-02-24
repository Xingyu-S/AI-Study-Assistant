from .api import GeminiClient
from .files import FileManager
from .storage import HistoryManager
from .prompts import PromptGenerator # 【新增】导入提示词模块

class ProjectAssistant:
    def __init__(self):
        self.api_client = GeminiClient()
        self.file_manager = FileManager()
        self.history_manager = HistoryManager()
        self.prompt_generator = PromptGenerator() # 【新增】初始化提示词生成器
        self.history = []

    def load_history(self, project_path):
        self.history = self.history_manager.load(project_path)
        return self.history

    def clear_active_history(self, project_path):
        self.history = [] 
        self.history_manager.clear(project_path) 

    def chat(self, user_text, project_path, image_data=None):
        """
        user_text: 用户问题
        image_data: Base64 编码的图片字符串
        """
        
        current_parts = [{"text": user_text}]

        # 1. 决定使用哪种提示词
        if image_data:
            # === 视觉模式 ===
            current_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_data
                }
            })
            # 从 prompts.py 获取视觉提示词
            system_instruction = self.prompt_generator.get_vision_prompt()
        else:
            # === 代码模式 ===
            file_context = self.file_manager.get_project_context(project_path)
            # 从 prompts.py 获取代码提示词，并传入文件内容
            system_instruction = self.prompt_generator.get_code_prompt(file_context)

        # 2. 构建 Payload
        payload = []
        
        # 插入系统提示 (仅在无历史记录时，或者你想每次都强调也行)
        if not self.history: 
             payload.append({"role": "user", "parts": [{"text": system_instruction}]})
             payload.append({"role": "model", "parts": [{"text": "好的，我明白了。"}]})

        # 注入历史
        for msg in self.history:
            role = "user" if msg['role'] == "user" else "model"
            payload.append({"role": role, "parts": [{"text": msg['text']}]})

        # 注入当前消息
        payload.append({"role": "user", "parts": current_parts})

        # 发送
        response_text = self.api_client.send_request(payload)

        # 保存
        self.history.append({"role": "user", "text": f"[用户发送了截图] {user_text}" if image_data else user_text})
        self.history.append({"role": "model", "text": response_text})
        self.history_manager.save(project_path, self.history)

        return response_text