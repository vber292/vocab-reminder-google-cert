# vocab-reminder-google-cert
A smart vocabulary learning assistant with spaced repetition algorithm
# Intelligent Vocabulary Learning System 🧠

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
[![Google Cert Progress](https://img.shields.io/badge/Google_Data_Analytics-40%25-orange)](https://grow.google/certificates/data-analytics/)

## 🛠️ Technical Architecture
```mermaid
flowchart TD
    A[CSV Input] --> B(Data Cleaning)
    B --> C{Mastery Level}
    C -->|Mastered| D[7-day Interval]
    C -->|Learning| E[3-day Interval]
    C -->|New| F[1-day Interval]
    
