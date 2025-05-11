import sys
import os

# 动态获取项目根目录（关键修复！）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.vocab_reminder_google_cert.main import VocabReminder
import unittest
# tests/test_main.py
def test_vocab_reminder():
    reminder = VocabReminder()
    assert reminder is not None
class TestVocabReminder(unittest.TestCase):
    def test_db(self):
        vr = VocabReminder()
        self.assertIsNotNone(vr.conn)

if __name__ == "__main__":
    unittest.main()
