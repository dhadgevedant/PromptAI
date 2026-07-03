import streamlit as st
from utils.llm import get_api_key

# 1. Page Configuration
st.set_page_config(
    page_title="Prompt Engineering Playground",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Notion-like clean aesthetics
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400&display=swap');
    
    /* Base Font Override to match Notion closely */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";
    }
    
    /* Simplify Titles */
    .gradient-text, .gold-gradient-text, .purple-gradient-text {
        font-weight: 700;
        color: inherit;
        background: none;
        -webkit-text-fill-color: initial;
    }
    
    /* Clean, flat cards (Notion-like) */
    .premium-card {
        background-color: transparent;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 6px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: none;
    }
    .premium-card:hover {
        border-color: rgba(128, 128, 128, 0.4);
    }
    
    /* Output Callouts (resembling Notion quotes/callouts) */
    .response-card, .cot-reasoning-card, .final-answer-box {
        background-color: rgba(128, 128, 128, 0.03);
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-left: 3px solid rgba(128, 128, 128, 0.5);
        border-radius: 4px;
        padding: 16px;
        margin-top: 12px;
        box-shadow: none;
    }
    
    .final-answer-box strong {
        font-weight: 600;
    }
    
    /* Code and Prompt styling */
    .prompt-card {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 4px;
        padding: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        white-space: pre-wrap;
        margin-top: 8px;
    }
    
    code {
        background-color: rgba(128, 128, 128, 0.1) !important;
        color: inherit !important;
        padding: 2px 4px !important;
        border-radius: 3px !important;
    }

    /* Flowchart and Tree Visualization Styles */
    .flow-card {
        border: 1px solid rgba(128, 128, 128, 0.4);
        border-radius: 6px;
        padding: 12px;
        margin: 0 auto;
        width: 80%;
        text-align: center;
        background-color: rgba(128, 128, 128, 0.05);
    }
    .flow-arrow {
        text-align: center;
        font-size: 24px;
        color: rgba(128, 128, 128, 0.6);
        margin: 5px 0;
        line-height: 1;
    }
    .tree-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 10px;
    }
    .tree-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        width: 100%;
        margin: 5px 0;
    }
    .tree-node {
        border: 1px solid rgba(128, 128, 128, 0.4);
        border-radius: 6px;
        padding: 12px;
        text-align: center;
        background-color: rgba(128, 128, 128, 0.05);
        flex: 1;
        font-size: 0.9rem;
    }
    .winner-node {
        border: 2px solid #28a745 !important;
        box-shadow: 0 0 10px rgba(40, 167, 69, 0.3);
        background-color: rgba(40, 167, 69, 0.05) !important;
    }
    .winner-badge {
        display: inline-block;
        background-color: #28a745;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-bottom: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration & API Key Input
st.sidebar.markdown("<h2 style='text-align: center;'>🛠️ Play Settings</h2>", unsafe_allow_html=True)

# Try fetching from environment
env_api_key = get_api_key()

if env_api_key:
    st.sidebar.success("🔑 Gemini API key loaded from environment.")
    api_key_to_use = env_api_key
else:
    st.sidebar.warning("⚠️ No API key found in `.env`.")
    api_key_to_use = st.sidebar.text_input(
        "Enter Gemini API Key:",
        type="password",
        help="Get an API key from Google AI Studio"
    )

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Visualizations")
st.sidebar.markdown("• CoT Flow Diagram")
st.sidebar.markdown("• Multi-Path Reasoning Tree")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Model")
st.sidebar.code("qwen3.5:4b (Local via Ollama)", language=None)
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🧠 Techniques Covered
1. **Zero & Few-Shot** — Page 1
   * No-example vs. example-guided prompting.
2. **Chain of Thought** — Page 2
   * Step-by-step thinking out loud, streamed in real time.
3. **Multi-Path Evaluator** — Page 3
   * Independent reasoning paths generated separately, then evaluated.
""")

# Store API key in session state for pages to access
st.session_state["api_key"] = api_key_to_use

# 4. Multi-page Navigation
zero_few_shot = st.Page("pages/zero_few_shot.py", title="Zero & Few-Shot", icon="🎯")
cot = st.Page("pages/cot.py", title="Chain of Thought", icon="🧠")
advanced_cot = st.Page("pages/advanced_cot.py", title="Multi-Path Reasoning", icon="🌳")

pg = st.navigation([zero_few_shot, cot, advanced_cot])
pg.run()
