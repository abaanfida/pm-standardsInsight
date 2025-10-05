import streamlit as st

# Set page config first
st.set_page_config(
    page_title="Standards Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin: 1rem 0;
        height: 100%;
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1f77b4;
    }
    .feature-description {
        color: #666;
        margin-bottom: 1.5rem;
    }
    .button-container {
        text-align: center;
        margin-top: auto;
    }
    .welcome-section {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Welcome Section
st.markdown("""
<div class="welcome-section">
    <h1>🚀 Standards Insights Dashboard</h1>
    <p style="font-size: 1.2rem; margin-bottom: 0;">Your comprehensive platform for project management standards analysis</p>
</div>
""", unsafe_allow_html=True)

# Features Introduction
st.markdown("""
### 📋 What You Can Do
Explore and analyze project management standards through our interactive tools. 
Compare methodologies, visualize coverage, and get AI-powered insights.
""")

# Three main features in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">Methodology Comparator</div>
        <div class="feature-description">
            Compare PMBOK 7, PRINCE2 7, and other standards across key topics. 
            Visualize coverage with heatmaps, radar charts, and interactive analysis.
        </div>
        <div class="button-container">
    """, unsafe_allow_html=True)
    if st.button("🎯 Open Comparator", key="comparator", use_container_width=True):
        st.switch_page("pages/0_Comparator.py")
    st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Dashboard & Analysis</div>
        <div class="feature-description">
            Deep dive into standards analytics. View comprehensive dashboards, 
            trend analysis, and detailed insights with interactive visualizations.
        </div>
        <div class="button-container">
    """, unsafe_allow_html=True)
    if st.button("📈 Open Dashboard", key="dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
    st.markdown("</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI Chatbot Assistant</div>
        <div class="feature-description">
            Get instant answers about project management standards. 
            Ask questions, get explanations, and receive guidance on methodology implementation.
        </div>
        <div class="button-container">
    """, unsafe_allow_html=True)
    if st.button("💬 Open Chatbot", key="chatbot", use_container_width=True):
        st.switch_page("pages/2_Chatbot.py")
    st.markdown("</div></div>", unsafe_allow_html=True)

# Quick Stats Section
st.markdown("---")
st.subheader("📈 Platform Overview")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric("Supported Standards", "3+", "PMBOK, PRINCE2, ISO...")

with stats_col2:
    st.metric("Analysis Topics", "30+", "Covering all domains")

with stats_col3:
    st.metric("Visualization Types", "8+", "Charts, maps, graphs")

with stats_col4:
    st.metric("AI-Powered", "Yes", "Smart insights")

# Features Grid with more details
st.markdown("---")
st.subheader("🎯 Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    **🔍 Methodology Comparator**
    - Side-by-side standard comparison
    - Coverage heatmaps and radar charts
    - Gap analysis and insights
    - Exportable reports
    
    **📊 Interactive Dashboard**
    - Real-time analytics
    - Trend visualization
    - Performance metrics
    - Customizable views
    """)

with feature_col2:
    st.markdown("""
    **🤖 AI Chatbot Assistant**
    - Natural language queries
    - Standard-specific guidance
    - Best practice recommendations
    - Implementation support
    
    **🔧 Advanced Tools**
    - Data export capabilities
    - Custom analysis setups
    - Team collaboration features
    - API integration ready
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 2rem;'>"
    "**Standards Insights Dashboard** • Built with Streamlit • "
    "<em>Empowering Better Project Management Decisions</em>"
    "</div>",
    unsafe_allow_html=True
)