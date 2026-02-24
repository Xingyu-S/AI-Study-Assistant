import os

class FileManager:
    def get_project_context(self, project_path):
        context_str = "以下是当前项目的完整文件内容：\n\n"
        count = 0 
        max_files = 30 
        
        ignore_dirs = ['.git', '__pycache__', '.idea', '.vscode', 'node_modules', '.ai_data']
        valid_exts = ('.py', '.txt', '.md', '.html', '.json', '.css', '.js', '.java', '.cpp', '.ipynb')

        for root, dirs, files in os.walk(project_path):
            # 过滤不需要的文件夹
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if count >= max_files: break
                if file.endswith(valid_exts) and file != "gemini_API.txt":
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            rel_path = os.path.relpath(file_path, project_path)
                            context_str += f"--- 文件名: {rel_path} ---\n{content}\n\n"
                            count += 1
                    except:
                        pass
        return context_str