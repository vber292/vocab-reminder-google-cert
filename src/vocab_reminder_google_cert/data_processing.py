# -*- coding: utf-8 -*-
# src/vocab_reminder_google_cert/data_processing.py

import os
import pandas as pd
import csv
from io import StringIO

def load_and_clean_data(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        raw_content = f.read()

    buffer = StringIO(raw_content)
    csv_reader = csv.reader(buffer)
    
    header = next(csv_reader)
    if header != ['word', 'definition']:
        raise ValueError(f"无效列名: {header}，必须为['word', 'definition']")

    for row_num, row in enumerate(csv_reader, 2):
        if len(row) != 2:
            raise ValueError(f"第{row_num}行格式错误，应有2列，实际{len(row)}列")

    buffer.seek(0)
    df = pd.read_csv(
        buffer,
        sep=',',
        header=None,
        names=['word', 'definition'],
        quoting=csv.QUOTE_ALL,
        skipinitialspace=True,
        engine='python'
    )

    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['word', 'definition'])
    df['word'] = df['word'].str.strip().str.lower()
    df = df.drop_duplicates(subset=['word'], keep='first')

    if df.empty:
        raise ValueError("清洗后数据为空！")

    return df