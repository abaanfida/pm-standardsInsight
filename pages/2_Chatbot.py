import streamlit as st
import requests
import pandas as pd
import time

# ==============================
# PAGE CONFIG - MUST BE FIRST
# ==============================
st.set_page_config(
    page_title="PM Chatbot Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==============================
# CONFIG
# ==============================
BACKEND_URL = "http://127.0.0.1:8000"

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
/* ===== GENERAL PAGE ===== */
body, .stApp {
    background-color: #0e1117 !important;  /* match Streamlit dark mode */
    color: #e0e0e0;
}

/* ===== MAIN HEADER ===== */
.main-header {
    text-align: center;
    padding: 1rem;
    border-bottom: 1px solid #2c2f36;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 8px;
    max-width: 900px;
    margin: auto;
}
.main-header h1 {
    font-size: 1.7rem;
    margin: 0;
}
.main-header p {
    font-size: 0.9rem;
    opacity: 0.9;
}

/* ===== CHAT CONTAINER ===== */
.chat-container {
    background: #1b1f26;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 1.5rem auto;
    border: 1px solid #2e3139;
    max-width: 850px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    color: #eaeaea;
}

/* ===== MESSAGES ===== */
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.9rem 1.2rem;
    border-radius: 16px 16px 5px 16px;
    margin: 0.8rem 0;
    max-width: 70%;
    margin-left: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.bot-message {
    background: #2a2f3a;
    color: #e6e6e6;
    padding: 0.9rem 1.2rem;
    border-radius: 16px 16px 16px 5px;
    margin: 0.8rem 0;
    max-width: 70%;
    border: 1px solid #3b3f48;
    box-shadow: 0 1px 5px rgba(0,0,0,0.2);
}
.message-time {
    font-size: 0.75rem;
    opacity: 0.7;
    text-align: right;
    margin-top: 0.3rem;
}

/* ===== INPUT AREA ===== */
.input-container {
    background: #1b1f26;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    border: 1px solid #2e3139;
    max-width: 800px;
    margin: 1rem auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.stTextInput input {
    background-color: #2a2f3a !important;
    color: #e6e6e6 !important;
    border: 1px solid #3b3f48 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1rem !important;
    font-size: 0.95rem !important;
}

.stButton > button {
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    font-size: 0.9rem !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.stButton > button:hover {
    opacity: 0.9;
}

/* ===== CLEAR BUTTON ===== */
.stButton:has(button:contains("Clear Conversation")) > button {
    background: #2a2f3a !important;
    color: #fff !important;
    border: 1px solid #3b3f48 !important;
}
.stButton:has(button:contains("Clear Conversation")) > button:hover {
    background: #3b3f48 !important;
}

/* ===== WELCOME MESSAGE ===== */
.welcome-message {
    text-align: center;
    padding: 2rem;
    background: #1b1f26;
    border-radius: 10px;
    border: 1px solid #2e3139;
    margin: 2rem auto;
    max-width: 700px;
    color: #ccc;
}
.welcome-message h3 {
    color: #fff;
}
</style>
""", unsafe_allow_html=True)



# ==============================
# SUGGESTED QUESTIONS
# ==============================
SUGGESTED_QUESTIONS = [
    "What are the key differences between PMBOK and PRINCE2?",
    "What is the role of a project manager in PRINCE2?",
    "Explain the concept of 'business case' in project management",
    "How do you manage stakeholders in a project?",
    "What are the main principles of PMBOK 7th edition?",
    "How does change control work in different methodologies?",
    "What is benefits management in project management?"
]

# ==============================
# INITIALIZE SESSION STATE
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "suggestions_used" not in st.session_state:
    st.session_state.suggestions_used = set()

# ==============================
# HELPER FUNCTIONS
# ==============================
def get_current_time():
    return time.strftime("%H:%M")

def add_message(role, content):
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "time": get_current_time()
    })

def send_chat_request(question):
    try:
        with st.spinner("🤔 Thinking..."):
            res = requests.post(f"{BACKEND_URL}/chat", json={"question": question})
            if res.status_code == 200:
                answer = res.json().get("answer", "No answer received.")
                return answer
            else:
                return f"❌ Error: {res.text}"
    except Exception as e:
        return f"❌ Failed to connect to server: {str(e)}"

# ==============================
# STREAMLIT UI
# ==============================

# Navigation
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Back to Home"):
        st.switch_page("Home.py")

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🤖 PROJECT MANAGEMENT CHATBOT ASSISTANT</h1>
    <p>Your AI-powered guide to project management standards and best practices</p>
</div>
""", unsafe_allow_html=True)

# Introduction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="stats-card">
        <h3>💡 ABOUT THIS CHATBOT</h3>
        <p>Ask me anything about project management methodologies, standards, best practices, 
        or specific topics from PMBOK, PRINCE2, ISO, and more. I'm here to help you understand 
        and navigate the world of project management!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stats-card">
        <h4>📊 CHAT STATS</h4>
        <p>💬 Messages: {}</p>
        <p>🎯 Suggestions: {}/8</p>
    </div>
    """.format(len(st.session_state.chat_history), len(st.session_state.suggestions_used)), unsafe_allow_html=True)

# Suggested Questions
st.markdown("### 💡 QUICK SUGGESTIONS")
st.markdown("<p style='color: #666; margin-bottom: 1rem;'>Click on any question below to get started:</p>", unsafe_allow_html=True)

suggestion_cols = st.columns(2)
for i, question in enumerate(SUGGESTED_QUESTIONS):
    with suggestion_cols[i % 2]:
        if st.button(
            question,
            key=f"suggest_{i}",
            use_container_width=True
        ):
            if question not in st.session_state.suggestions_used:
                st.session_state.suggestions_used.add(question)
            add_message("user", question)
            answer = send_chat_request(question)
            add_message("assistant", answer)
            st.rerun()

# Chat Container
st.markdown("### 💬 CONVERSATION")
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #666;">
        <h3>👋 Hello! I'm your PM Assistant</h3>
        <p>Start a conversation by typing a question below or clicking one of the suggestions above.</p>
        <p>I can help with PMBOK, PRINCE2, Agile, risk management, stakeholder management, and more!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div style="font-weight: bold; margin-bottom: 0.5rem;">👤 YOU</div>
                <div>{message['content']}</div>
                <div class="message-time">{message['time']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bot-message">
                <div style="font-weight: bold; margin-bottom: 0.5rem;">🤖 PM ASSISTANT</div>
                <div>{message['content']}</div>
                <div class="message-time">{message['time']}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-container">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    user_question = st.text_input(
        "Type your question here:",
        placeholder="Ask about PMBOK, PRINCE2, Agile, risk management, stakeholders...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    ask_clicked = st.button("🚀 Send", use_container_width=True)

if ask_clicked and user_question.strip():
    add_message("user", user_question)
    answer = send_chat_request(user_question)
    add_message("assistant", answer)
    st.rerun()
elif ask_clicked and not user_question.strip():
    st.warning("📝 Please enter a question before sending.")

st.markdown('</div>', unsafe_allow_html=True)

# Clear Chat Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.suggestions_used = set()
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "🤖 PM Chatbot Assistant • Powered by AI • Your Guide to Project Management Excellence"
    "</div>",
    unsafe_allow_html=True
)