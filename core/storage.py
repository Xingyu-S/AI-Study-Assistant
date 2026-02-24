import os
import json

class HistoryManager:
    def __init__(self):
        self.folder_name = ".ai_data" # 独立的隐藏文件夹
        self.history_file = "chat_history.json"
        self.config_file = "config.json" # 【新增】配置文件

    def _get_folder(self, project_path):
        data_dir = os.path.join(project_path, self.folder_name)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return data_dir

    def _get_history_path(self, project_path):
        return os.path.join(self._get_folder(project_path), self.history_file)

    def _get_config_path(self, project_path):
        return os.path.join(self._get_folder(project_path), self.config_file)

    # --- 历史记录相关 ---
    def load(self, project_path):
        file_path = self._get_history_path(project_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []

    def save(self, project_path, history_data):
        file_path = self._get_history_path(project_path)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def clear(self, project_path):
        file_path = self._get_history_path(project_path)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except:
                return False
        return True

    # --- 【新增】配置记忆相关 (存网址) ---
    def load_config(self, project_path):
        """读取配置文件"""
        file_path = self._get_config_path(project_path)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {} # 默认返回空字典

    def save_config(self, project_path, config_data):
        """保存配置文件"""
        file_path = self._get_config_path(project_path)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
        except:
            pass