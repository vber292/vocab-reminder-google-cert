# Course4: 数据可视化

import matplotlib.pyplot as plt
import sqlite3
import pandas as pd

def generate_report():
    # Course3: SQL查询
    conn = sqlite3.connect('data/learning.db')
    df = pd.read_sql("""
        SELECT 
            strftime('%Y-%m-%d', timestamp) as date,
            COUNT(*) as count 
        FROM learning_log 
        GROUP BY date
    """, conn)
    
    # Course4 Week2: Matplotlib可视化
    plt.style.use('ggplot')
    df.plot(x='date', y='count', kind='bar', title='每日学习统计')
    plt.savefig('docs/daily_report.png')
    print("报告已生成: docs/daily_report.png")

if __name__ == "__main__":
    generate_report()