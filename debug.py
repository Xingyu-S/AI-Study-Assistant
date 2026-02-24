import requests
import json

# 1. 读取你的 API Key
try:
    with open("gemini_API.txt", "r", encoding="utf-8") as f:
        key = f.read().strip()
except:
    print("找不到 API Key 文件！")
    exit()

# 2. 向谷歌询问：请列出所有我能用的模型
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
response = requests.get(url)

# 3. 打印结果
if response.status_code == 200:
    models = response.json().get('models', [])
    print("--- 你的可用模型列表 ---")
    for m in models:
        # 只显示支持生成内容的模型
        if "generateContent" in m.get('supportedGenerationMethods', []):
            print(f"名称: {m['name']}")
    print("------------------------")
else:
    print("查询失败，错误信息：")
    print(response.text)