import sys
import os

# 动态获取项目根目录（关键修复！）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import VocabReminder
import unittest

class TestVocabReminder(unittest.TestCase):
    def test_db(self):
        vr = VocabReminder()
        self.assertIsNotNone(vr.conn)

if __name__ == "__main__":
    unittest.main()
