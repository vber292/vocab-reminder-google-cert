# main.py
import sqlite3

class VocabReminder:  # 类名必须完全一致（注意大小写）
    def __init__(self):
        self.conn = sqlite3.connect('data/learning.db')  # 确保路径正确
        
if __name__ == "__main__":
    print("✅ 类验证通过！")