import os
import requests
import json

class GeminiClient:
    def __init__(self):
        self.api_key = self._load_api_key()
        # 【修正】改回你的账号唯一能用的名字：gemini-flash-latest
        self.url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

    def _load_api_key(self):
        try:
            if os.path.exists("gemini_API.txt"):
                with open("gemini_API.txt", "r", encoding="utf-8") as f:
                    return f.read().strip()
        except:
            pass
        return None

    def send_request(self, messages_payload):
        """
        发送请求给 Gemini
        messages_payload: 已经包含文本或图片数据的列表
        """
        if not self.api_key:
            return "错误：缺少 API Key"

        full_url = f"{self.url}?key={self.api_key}"
        headers = {'Content-Type': 'application/json'}
        data = { "contents": messages_payload }

        try:
            # 增加 timeout 防止传图片时网络卡顿
            response = requests.post(full_url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"API Error {response.status_code}: {response.text}"
        except Exception as e:
            return f"Network Error: {str(e)}"