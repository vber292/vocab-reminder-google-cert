import pytest
from src.vocab_reminder_google_cert.data_processing import load_and_clean_data

def test_data_cleaning():
    df = load_and_clean_data("data/raw_vocab.csv")
    assert df.duplicated().sum() == 0
