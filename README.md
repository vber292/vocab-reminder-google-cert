# vocab-reminder-google-cert
A smart vocabulary learning assistant with spaced repetition algorithm
# Intelligent Vocabulary Learning System 🧠

## Google Data Analysis Course Mapping
| Project Feature        | Course Module                | Technical Implementation |
|-------------------------|-------------------------------|---------------------------|
| Learning Data Cleaning  | Data Cleaning & Preparation   | \`pandas.dropna()\`         |
| Review Interval Optimization | Descriptive Analytics    | \`matplotlib.plot()\`       |
| A/B Testing Framework   | Experimental Design           | \`scipy.stats.ttest_ind()\` |
# Vocabulary Reminder
**Smart Vocabulary Learning System with Spaced Repetition**
*(Melbourne University COMP90041 & Google Data Analysis Professional Certificate Project)*
 
<img src="assets/screenshots/1.png" alt="System Interface" width="800">
*Fig.1 - Main interface showing learning statistics and review schedule*
 
## Project Context
This project integrates spaced repetition algorithm implementation (COMP90041) with Google Data Analysis techniques:
- Applied **data cleaning** (Pandas) on user learning history
- Conducted **descriptive analytics** to optimize review intervals
- Visualized learning patterns using **Matplotlib/Seaborn**
- Implemented A/B testing framework for algorithm comparison
 
## Core Features
1. Adaptive learning schedule via SM-2 algorithm
2. Multi-device sync with Google Calendar API
3. Custom vocabulary library management
4. Learning analytics dashboard (Word retention rate/Review frequency)
 
## Technical Stack
- Frontend: Vue.js 3 + TypeScript
- Backend: Flask 2.3 + SQLite
- Data Analysis: Pandas 1.5 + Matplotlib 3.7
- Deployment: Docker Compose 
*Certificate verification:* [Google Data Analysis Professional Certificate](https://www.coursera.org/account/accomplishments/certificate/YOUR_CERT_ID)
" >> README.md
 
# 6. 提交变更
git add README.md
git commit -m "docs: Add Google course mapping and academic validation"
 
# 7. 推送分支
git push origin feature/readme-update
 
# 8. 创建Pull Request（网页操作）


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
    
