# 🧠 Project Management Insight Dashboard

## 📘 Overview
The **Project Management Insight Dashboard** is an intelligent web application that helps users **analyze, compare, and gain insights** from different **Project Management Standards** (such as PMBOK, PRINCE2, ISO 21500, etc.).  

It enables users to:
- 🔍 **Search and compare** specific sections or topics across multiple PM standards.  
- 📊 **Visualize similarities and differences** between methodologies and concepts.  
- 🤖 **Chat with an AI-powered assistant** to answer project management-related questions in real time.

---

## 🚀 Features

### 🔎 Standard Comparison
- Search across multiple PM standards for a topic or section.  
- Compare overlapping methodologies, terminologies, and processes.  
- Identify **unique points** and **common practices** across standards.

### 📈 Insights Dashboard
- Interactive **visual summaries** using **Plotly** and **Pandas**.  
- Highlight similarities, differences, and gaps in project management coverage.  
- Dynamic data-driven analysis of multiple frameworks.

### 💬 AI Chatbot Assistant
- Powered by **Groq + FastAPI** backend.  
- Answers project management questions conversationally.  
- References extracted standard sections for accurate responses.


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
git clone https://github.com/abaanfida/pm-standardsInsight.git
cd pm-standardsInsight
### Dependencies
pip install sqlalchemy database pymupdf fastapi streamlit time pandas plotly groq pydantic
### Run
uvicorn backend:app --reload

streamlit run Home.py

