import streamlit as st
import requests
import pandas as pd

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Standards Comparison", layout="wide")
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

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
    }
    .standard-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .result-count {
        background: #ff4b4b;
        color: white;
        border-radius: 20px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
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
    .no-results {
        text-align: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 2px dashed #dee2e6;
        color: #6c757d;
    }
    .search-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-item {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# FETCH STANDARDS DYNAMICALLY
# ==============================
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

# ==============================
# HELPER FUNCTIONS
# ==============================
def format_section_title(title):
    """Convert section title to uppercase and clean formatting"""
    if not title or pd.isna(title):
        return "CONTENT SECTION"
    return str(title).strip().upper()

def create_result_card(title, content, standard_name, result_number):
    """Create a nicely formatted result card"""
    formatted_title = format_section_title(title)
    
    card_html = f"""
    <div class="result-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <h4 style="margin: 0; color: #1f77b4;">{formatted_title}</h4>
            <span style="background: #667eea; color: white; border-radius: 12px; padding: 0.25rem 0.75rem; font-size: 0.8rem; font-weight: bold;">
                #{result_number}
            </span>
        </div>
        <div style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">
            <strong>Standard:</strong> {standard_name}
        </div>
        <div style="color: #333; line-height: 1.5;">
            {content[:300] + "..." if len(content) > 300 else content}
        </div>
    </div>
    """
    return card_html

# ==============================
# SEARCH FUNCTION
# ==============================
def search_standard(standard_name, query):
    try:
        response = requests.get(f"{BACKEND_URL}/search", params={"q": query, "standard_name": standard_name})
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and data:
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([{"title": "No results found", "content": f"No matches for '{query}' in {standard_name}"}])
        else:
            return pd.DataFrame([{"title": "Search Error", "content": f"API returned status {response.status_code}"}])
    except Exception as e:
        return pd.DataFrame([{"title": "Connection Error", "content": f"Could not connect to backend: {str(e)}"}])

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
    <h1>🔍 STANDARDS COMPARISON TOOL</h1>
    <p>Compare project management standards side-by-side</p>
</div>
""", unsafe_allow_html=True)

# Get available standards from backend
available_standards = get_standards()

if not available_standards:
    st.warning("⚠️ No standards found in the backend. Please add some first.")
else:
    # Search Section
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    st.markdown("### 📝 SEARCH PARAMETERS")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input(
            "Enter search term:",
            placeholder="e.g., 'risk management', 'project planning', 'quality control'...",
            help="Search for specific topics across all selected standards"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        compare_btn = st.button(
            "🔍 COMPARE STANDARDS", 
            type="primary", 
            use_container_width=True
        )
    
    # Standards Selection
    st.markdown("### 📚 SELECT STANDARDS TO COMPARE")
    standards = st.multiselect(
        "Choose standards:",
        options=available_standards,
        default=available_standards[:2],
        label_visibility="collapsed"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ==============================
    # DISPLAY RESULTS
    # ==============================
    if compare_btn:
        if not search_query.strip():
            st.warning("🚨 Please enter a search term to compare standards.")
        elif not standards:
            st.warning("🚨 Please select at least one standard to compare.")
        else:
            # Results Header
            st.markdown(f"""
            <div class="section-header">
                📊 COMPARISON RESULTS FOR: "{search_query.upper()}"
            </div>
            """, unsafe_allow_html=True)
            
            # Create columns for each standard
            cols = st.columns(len(standards))
            
            # Store all results for summary
            all_results = {}
            
            for i, standard in enumerate(standards):
                with cols[i]:
                    # Standard Header with Count
                    results_df = search_standard(standard, search_query)
                    result_count = len(results_df) if not results_df.empty else 0
                    
                    st.markdown(f"""
                    <div class="standard-card">
                        <h3 style="margin: 0; display: flex; align-items: center;">
                            {standard}
                            <span class="result-count">{result_count}</span>
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    all_results[standard] = results_df
                    
                    # Display Results
                    if results_df.empty:
                        st.markdown("""
                        <div class="no-results">
                            <h4>📭 NO RESULTS</h4>
                            <p>No matching content found in this standard</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        for idx, row in results_df.iterrows():
                            title = row.get("title", "Content Section")
                            content = row.get("content", "No content available")
                            
                            result_card = create_result_card(
                                title, 
                                content, 
                                standard, 
                                idx + 1
                            )
                            st.markdown(result_card, unsafe_allow_html=True)
            
            # ==============================
            # SUMMARY STATISTICS
            # ==============================
            st.markdown("""
            <div class="section-header">
                📈 COMPARISON SUMMARY
            </div>
            """, unsafe_allow_html=True)
            
            # Create summary metrics
            summary_cols = st.columns(len(standards) + 1)
            
            total_results = 0
            for i, standard in enumerate(standards):
                with summary_cols[i]:
                    result_count = len(all_results[standard])
                    total_results += result_count
                    st.metric(
                        label=f"{standard} Results",
                        value=result_count,
                        delta=None
                    )
            
            with summary_cols[-1]:
                st.metric(
                    label="Total Results",
                    value=total_results,
                    delta="All Standards"
                )
            
            # Detailed Summary
            with st.expander("📋 DETAILED ANALYSIS SUMMARY", expanded=False):
                for standard in standards:
                    results_df = all_results[standard]
                    if not results_df.empty:
                        st.subheader(f"📖 {standard} - Found Sections:")
                        sections = results_df.get("title", pd.Series(["Content Sections"])).tolist()
                        for j, section in enumerate(sections, 1):
                            st.write(f"{j}. **{format_section_title(section)}**")
                    else:
                        st.write(f"**{standard}**: No relevant sections found")
            
            # Export Option
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.info("💡 **Tip**: Use the expanders above to view detailed content from each standard. Results are displayed in order of relevance.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "🔍 Standards Comparison Tool • Search and compare project management standards efficiently"
    "</div>",
    unsafe_allow_html=True
)