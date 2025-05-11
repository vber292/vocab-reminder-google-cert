# -*- coding: utf-8 -*-
# src/vocab_reminder_google_cert/main.py

import datetime
import os
import sqlite3
import pandas as pd
from typing import Tuple, Optional
from .data_processing import load_and_clean_data

class VocabReminder:
    def __init__(self):
        self.conn = sqlite3.connect('data/vocab.db')
        self.cursor = self.conn.cursor()
        self._init_database()
        self._load_words()

    def _init_database(self) -> None:
        """初始化数据库表结构"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                word TEXT PRIMARY KEY,
                definition TEXT,
                mastery INTEGER DEFAULT 0,
                review_count INTEGER DEFAULT 0,
                correct_count INTEGER DEFAULT 0,
                last_reviewed DATETIME,
                next_review DATETIME DEFAULT (datetime('now', '+1 day'))
            )
        ''')
        self.conn.commit()

    def get_random_word(self) -> Tuple[str, str]:
        """获取需要复习的随机单词"""
        self.cursor.execute('''
            SELECT word, definition 
            FROM words 
            WHERE next_review <= datetime('now')
            ORDER BY RANDOM() 
            LIMIT 1
        ''')
        result = self.cursor.fetchone()
        if not result:
            raise ValueError("数据库中没有需要复习的单词！")
        return result

    def update_review_stats(self, word: str, is_correct: bool) -> None:
        """更新单词复习统计信息"""
        interval = self._calculate_interval(word)
        self.cursor.execute('''
            UPDATE words 
            SET 
                review_count = review_count + 1,
                correct_count = correct_count + ? ,
                last_reviewed = datetime('now'),
                next_review = datetime('now', ?)
            WHERE word = ?
        ''', (1 if is_correct else 0, f"+{interval} days", word))
        self.conn.commit()

    def _calculate_interval(self, word: str) -> int:
        """计算下次复习间隔"""
        self.cursor.execute('''
            SELECT 
                CASE 
                    WHEN review_count = 0 THEN 1
                    WHEN (correct_count * 1.0 / review_count) >= 0.9 THEN 7
                    WHEN (correct_count * 1.0 / review_count) >= 0.7 THEN 3
                    ELSE 1
                END AS interval
            FROM words 
            WHERE word = ?
        ''', (word,))
        return self.cursor.fetchone()[0]

    def _load_words(self) -> None:
        """从CSV加载单词数据"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, '..', '..', 'data', 'raw_vocab.csv')

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV 文件不存在！路径: {csv_path}")

        df = load_and_clean_data(csv_path)
        insert_data = [(word, defn) for word, defn in df.values]
        
        self.cursor.executemany('''
            INSERT OR IGNORE INTO words (word, definition)
            VALUES (?, ?)
        ''', insert_data)
        self.conn.commit()

def print_word_stats() -> None:
    """打印数据库统计信息"""
    vr = VocabReminder()
    df = pd.read_sql("SELECT * FROM words", vr.conn)
    print("\n当前单词统计：")
    print(f"总单词数: {len(df)}")
    print(f"待复习单词: {len(df[df['next_review'] <= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])}")
    print("\n示例数据预览：")
    print(df[['word', 'definition', 'next_review']].head().to_string(index=False))
if __name__ == "__main__":
    print("=== 单词背诵系统 - 测试模式 ===")
    print("1. 初始化数据库...")
    vr = VocabReminder()
    print("2. 加载示例数据...")
    print("3. 显示数据库统计：")
    print_word_stats()
    print("=============================")