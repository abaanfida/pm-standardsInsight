import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==============================
# PAGE CONFIG - MUST BE FIRST
# ==============================
st.set_page_config(
    page_title="Methodology Coverage Dashboard", 
    page_icon="📊", 
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
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #e6e6e6;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid #ff4b4b;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
    }
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;
    }
    .observation-success {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #333333;
    }
    .observation-warning {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #333333;
    }
    .observation-info {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #333333;
    }
    .observation-error {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        color: #333333;
    }
    .tab-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Updated topics list from previous response
PROJECT_MANAGEMENT_TOPICS = [
    # PMBOK 7th Edition: Project Performance Domains 
    "Stakeholders", "Team", "Development Approach and Life Cycle", "Planning",
    "Project Work", "Delivery", "Measurement", "Uncertainty",
    # PMBOK 7th Edition: Core Principles & Concepts 
    "Stewardship", "Value Delivery", "Tailoring", "Models, Methods, and Artifacts",
    # PRINCE2 7th Edition: Practices (formerly Themes) 
    "Business Case", "Organizing", "Quality", "Risk", "Issues", "Progress",
    # PRINCE2 7th Edition: Processes 
    "Starting up a Project", "Directing a Project", "Initiating a Project",
    "Controlling a Stage", "Managing Product Delivery", "Managing a Stage Boundary", "Closing a Project",
    # PRINCE2 7th Edition: Principles 
    "Continued Business Justification", "Learn from Experience", "Defined Roles and Responsibilities",
    "Manage by Stages", "Manage by Exception", "Focus on Products", "Tailor to Suit the Project Environment",
    # Common & Cross-Cutting Topics
    "Change Control", "Agile Practices", "Project Governance", "Lessons Learned",
    "Benefits Management", "Sustainability"
]

@st.cache_data
def get_standards():
    try:
        response = requests.get(f"{BACKEND_URL}/standards")
        if response.status_code == 200:
            data = response.json()
            return [item["name"] for item in data]
        else:
            st.error(f"Failed to fetch standards: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return []

def create_coverage_heatmap(df, standards):
    """Create a heatmap showing coverage intensity"""
    # Prepare data for heatmap
    heatmap_data = df.set_index('Topic')[standards]
    
    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Standard", y="Topic", color="Coverage Count"),
        x=standards,
        y=df['Topic'].tolist(),
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    
    fig.update_layout(
        title={
            'text': "METHODOLOGY COVERAGE HEATMAP",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f77b4'}
        },
        xaxis_title="STANDARDS",
        yaxis_title="TOPICS",
        height=800,
        coloraxis_colorbar=dict(title="COVERAGE<br>INTENSITY"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    # Add annotations
    for i, topic in enumerate(df['Topic']):
        for j, std in enumerate(standards):
            value = heatmap_data.iloc[i, j]
            if value > 0:
                fig.add_annotation(
                    x=j, y=i,
                    text=str(value),
                    showarrow=False,
                    font=dict(color="white" if value > heatmap_data.values.max()/2 else "black", size=10)
                )
    
    return fig

def create_radar_chart(coverage_data, standards):
    """Create a radar chart comparing standards across topic categories"""
    
    # Categorize topics for radar chart
    categories = {
        "PERFORMANCE DOMAINS": ["Stakeholders", "Team", "Development Approach and Life Cycle", 
                               "Planning", "Project Work", "Delivery", "Measurement", "Uncertainty"],
        "PRINCIPLES & GOVERNANCE": ["Stewardship", "Value Delivery", "Tailoring", "Models, Methods, and Artifacts",
                                   "Project Governance", "Sustainability"],
        "PRINCE2 PRACTICES": ["Business Case", "Organizing", "Quality", "Risk", "Issues", "Progress"],
        "PROCESSES & LIFECYCLE": ["Starting up a Project", "Directing a Project", "Initiating a Project",
                                 "Controlling a Stage", "Managing Product Delivery", 
                                 "Managing a Stage Boundary", "Closing a Project"],
        "CROSS-CUTTING TOPICS": ["Change Control", "Agile Practices", "Lessons Learned", 
                         "Benefits Management"]
    }
    
    # Calculate average coverage for each category
    radar_data = []
    
    for std in standards:
        std_coverage = []
        for category, topics in categories.items():
            # Get coverage for topics in this category
            coverage_values = []
            for topic in topics:
                if topic in [item['Topic'] for item in coverage_data]:
                    topic_data = next(item for item in coverage_data if item['Topic'] == topic)
                    coverage_values.append(topic_data.get(std, 0))
            
            if coverage_values:
                # Normalize the average (assuming max possible coverage per topic is 10 for scaling)
                avg_coverage = sum(coverage_values) / len(coverage_values)
                normalized_coverage = min(avg_coverage / 10 * 100, 100)  # Scale to percentage
                std_coverage.append(normalized_coverage)
            else:
                std_coverage.append(0)
        
        radar_data.append(go.Scatterpolar(
            r=std_coverage + [std_coverage[0]],  # Close the radar
            theta=list(categories.keys()) + [list(categories.keys())[0]],
            fill='toself',
            name=std,
            opacity=0.8
        ))
    
    fig = go.Figure(data=radar_data)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        title={
            'text': "STANDARD COVERAGE BY CATEGORY",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f77b4'}
        },
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

def create_coverage_comparison(df, standards):
    """Create bar chart comparing total coverage by standard"""
    total_coverage = df[standards].sum()
    
    fig = px.bar(
        x=standards,
        y=total_coverage.values,
        color=standards,
        title="TOTAL COVERAGE COMPARISON BY STANDARD",
        labels={"x": "STANDARD", "y": "TOTAL COVERAGE COUNT"},
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    return fig

def create_topic_coverage_bubble(df, standards):
    """Create bubble chart showing topic coverage across standards"""
    # Prepare data for bubble chart
    bubble_data = []
    for _, row in df.iterrows():
        for std in standards:
            bubble_data.append({
                'Topic': row['Topic'],
                'Standard': std,
                'Coverage': row[std],
                'Size': row[std] * 20  # Scale for bubble size
            })
    
    bubble_df = pd.DataFrame(bubble_data)
    
    fig = px.scatter(
        bubble_df,
        x='Standard',
        y='Topic',
        size='Size',
        color='Coverage',
        color_continuous_scale='viridis',
        title="TOPIC COVERAGE BUBBLE CHART",
        labels={'Coverage': 'COVERAGE INTENSITY', 'Standard': 'STANDARD', 'Topic': 'TOPIC'},
        size_max=40
    )
    
    fig.update_layout(
        height=800,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="STANDARD",
        yaxis_title="TOPIC"
    )
    return fig

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
    <h1>📊 METHODOLOGY COVERAGE DASHBOARD</h1>
    <p>Comprehensive Analysis of Project Management Standards Coverage</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="metric-card">
    <h3>🎯 ABOUT THIS DASHBOARD</h3>
    <p>This dashboard provides a comprehensive comparison of how different project management 
    standards cover key topics and domains. Analyze coverage patterns, identify gaps, and 
    understand the strengths of each methodology.</p>
</div>
""", unsafe_allow_html=True)

available_standards = get_standards()
if not available_standards:
    st.warning("⚠️ No standards found in the backend.")
else:
    # Selection Section
    st.markdown("""
    <div class="section-header">
        ⚙️ ANALYSIS CONFIGURATION
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        standards = st.multiselect(
            "SELECT STANDARDS TO ANALYZE:",
            options=available_standards,
            default=available_standards[:2] if len(available_standards) >= 2 else available_standards,
            help="Choose multiple standards to compare their coverage across topics"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button(
            "🔍 ANALYZE COVERAGE", 
            type="primary", 
            use_container_width=True,
        )

    if analyze_btn:
        if len(standards) < 2:
            st.warning("🚨 Please select at least two standards for comparison.")
        else:
            # Data collection
            with st.spinner("🔄 Analyzing standards coverage..."):
                coverage_data = []
                progress_bar = st.progress(0)
                total_topics = len(PROJECT_MANAGEMENT_TOPICS)
                
                for idx, topic in enumerate(PROJECT_MANAGEMENT_TOPICS):
                    row = {"Topic": topic}
                    for std in standards:
                        res = requests.get(f"{BACKEND_URL}/search", params={"q": topic, "standard_name": std})
                        if res.status_code == 200:
                            data = res.json()
                            count = len(data) if isinstance(data, list) else 0
                            row[std] = count
                        else:
                            row[std] = 0
                    coverage_data.append(row)
                    progress_bar.progress((idx + 1) / total_topics)

            df = pd.DataFrame(coverage_data)
            
            # Summary Metrics
            st.markdown("""
            <div class="section-header">
                📈 QUICK STATISTICS
            </div>
            """, unsafe_allow_html=True)
            
            metric_cols = st.columns(len(standards) + 2)
            
            with metric_cols[0]:
                total_coverage = df[standards].sum().sum()
                st.metric("Total Coverage Points", total_coverage)
            
            for i, std in enumerate(standards, 1):
                with metric_cols[i]:
                    std_coverage = df[std].sum()
                    coverage_pct = (df[std] > 0).sum() / len(df) * 100
                    st.metric(
                        f"{std} Coverage", 
                        f"{std_coverage}",
                        f"{coverage_pct:.1f}% topics"
                    )
            
            with metric_cols[-1]:
                common_topics = sum(1 for topic_row in coverage_data 
                                  if all(topic_row.get(std, 0) > 0 for std in standards))
                st.metric("Common Topics", common_topics)
            
            # Display visualizations in tabs
            st.markdown("""
            <div class="section-header">
                📊 VISUAL ANALYSIS
            </div>
            """, unsafe_allow_html=True)
            
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 DATA TABLE", 
                "🔥 COVERAGE HEATMAP", 
                "📈 RADAR ANALYSIS", 
                "📊 STANDARD COMPARISON", 
                "🫧 TOPIC BUBBLE CHART"
            ])

            with tab1:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)
                
                # Enhanced observations section
                st.markdown("### 🧩 COVERAGE OBSERVATIONS")
                
                for topic_row in coverage_data:
                    present = [std for std in standards if topic_row.get(std, 0) > 0]
                    topic_name = topic_row['Topic']
                    
                    if len(present) == len(standards):
                        st.markdown(f"""
                        <div class="observation-success">
                            ✅ <strong>{topic_name}</strong> is comprehensively covered across ALL selected standards.
                        </div>
                        """, unsafe_allow_html=True)
                    elif len(present) == 1:
                        st.markdown(f"""
                        <div class="observation-warning">
                            🌟 <strong>{topic_name}</strong> is uniquely covered by <strong>{present[0]}</strong>.
                        </div>
                        """, unsafe_allow_html=True)
                    elif len(present) > 1:
                        st.markdown(f"""
                        <div class="observation-info">
                            🔁 <strong>{topic_name}</strong> is shared between: <strong>{', '.join(present)}</strong>.
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="observation-error">
                            ❌ <strong>{topic_name}</strong> has no coverage in any selected standard.
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.plotly_chart(create_coverage_heatmap(df, standards), use_container_width=True)
                st.markdown("""
                **🔥 HEATMAP INTERPRETATION GUIDE:**
                - 🟣 **Darker Purple** = Higher coverage intensity and more comprehensive treatment
                - 🟡 **Lighter Colors** = Lower coverage or minimal treatment
                - 🔢 **Numbers** = Exact coverage count references
                - 📊 **Use** = Quick visual identification of coverage patterns and gaps
                """)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab3:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.plotly_chart(create_radar_chart(coverage_data, standards), use_container_width=True)
                st.markdown("""
                **📈 RADAR CHART INSIGHTS:**
                - 📐 **Larger Area** = More comprehensive coverage in those categories
                - 🔄 **Overlapping Areas** = Shared strengths between standards
                - 📍 **Spikes** = Particular strengths in specific categories
                - 🎯 **Use** = Compare categorical coverage patterns at a glance
                """)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab4:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(create_coverage_comparison(df, standards), use_container_width=True)
                with col2:
                    st.markdown("### 📊 COVERAGE BREAKDOWN")
                    for std in standards:
                        coverage_pct = (df[std] > 0).sum() / len(df) * 100
                        avg_coverage = df[std].mean()
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{std}</h4>
                            <p>📖 <strong>Topic Coverage:</strong> {coverage_pct:.1f}%</p>
                            <p>📊 <strong>Average Depth:</strong> {avg_coverage:.1f} references</p>
                            <p>🔢 <strong>Total References:</strong> {df[std].sum()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with tab5:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.plotly_chart(create_topic_coverage_bubble(df, standards), use_container_width=True)
                st.markdown("""
                **🫧 BUBBLE CHART GUIDE:**
                - 💠 **Larger Bubbles** = Higher coverage intensity and more extensive treatment
                - 🎨 **Darker Colors** = Greater coverage density
                - 📍 **Vertical Position** = Specific topic area
                - ➡️ **Horizontal Position** = Standard being analyzed
                - 🔍 **Use** = Identify coverage concentration and topic-standard relationships
                """)
                st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "📊 Methodology Coverage Dashboard • Professional Standards Analysis Tool"
    "</div>",
    unsafe_allow_html=True
)