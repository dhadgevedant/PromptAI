"""
Page 3 – Multi-Path Reasoning Evaluator
Uses: Gemini Flash Lite (gemini-1.5-flash-8b) with real-time streaming.
"""

import streamlit as st
import re
import graphviz
import textwrap
from utils.prompts import PAGE3_SAMPLES, get_path_prompt, get_evaluator_prompt
from utils.llm import generate_stream

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🌳 Multi-Path Reasoning Evaluator")
st.markdown(
    "Generate **multiple independent solutions**, let the model evaluate them, "
    "and visually map the *Tree of Thoughts* using Graphviz."
)

st.divider()

# ── Sample quick-fill buttons ─────────────────────────────────────────────────
st.markdown("**📋 Sample Problems** — click to load one")
cols = st.columns(len(PAGE3_SAMPLES))
for idx, (title, content) in enumerate(PAGE3_SAMPLES.items()):
    if cols[idx].button(title, use_container_width=True, key=f"p3_sample_{idx}"):
        st.session_state["p3_problem"] = content

# ── Inputs ────────────────────────────────────────────────────────────────────
default_p = st.session_state.get(
    "p3_problem",
    "A bat and a ball cost ₹110. The bat costs ₹100 more than the ball. What is the price of the ball?"
)
problem_input = st.text_area(
    "Enter your complex problem:",
    value=default_p,
    height=100
)

num_paths = st.slider(
    "Number of reasoning paths:",
    min_value=2,
    max_value=5,
    value=3
)

generate_btn = st.button("🌳 Generate & Evaluate", type="primary", use_container_width=True)

# ── Generation ────────────────────────────────────────────────────────────────
if generate_btn:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.error("🔑 Please enter your Gemini API Key in the sidebar to continue.")
    elif not problem_input.strip():
        st.warning("Please enter a problem first.")
    else:
        st.divider()
        
        # Placeholders for structured layout
        tree_placeholder = st.empty()
        
        st.markdown("### 🔍 Detailed Path Cards")
        paths_container = st.container()
        
        st.markdown("### ⚖️ Evaluation & Final Answer")
        eval_container = st.container()
        
        collected_paths: list[str] = []
        path_conclusions: list[str] = []

        # ── Step 1: Generate each path independently (streamed) ───────────
        with paths_container:
            for path_num in range(1, num_paths + 1):
                with st.expander(f"▼ Path {path_num}", expanded=True):
                    prompt = get_path_prompt(problem_input, path_num, num_paths)
                    placeholder = st.empty()
                    path_text = ""
                    try:
                        for chunk in generate_stream(prompt, api_key):
                            path_text += chunk
                            placeholder.markdown(path_text + " ▌")
                        placeholder.markdown(path_text)
                        collected_paths.append(path_text)
                        
                        # Extract a simple conclusion (last non-empty paragraph)
                        paragraphs = [p for p in path_text.split('\n') if p.strip()]
                        conclusion = paragraphs[-1] if paragraphs else "No conclusion."
                        path_conclusions.append(conclusion)
                        
                    except Exception as e:
                        st.error(f"Gemini API error on Path {path_num}: {e}")
                        st.stop()

        # ── Step 2: Evaluator call (streamed) ─────────────────────────────
        with eval_container:
            evaluator_prompt = get_evaluator_prompt(problem_input, collected_paths)
            eval_placeholder = st.empty()
            eval_text = ""
            try:
                for chunk in generate_stream(evaluator_prompt, api_key):
                    eval_text += chunk
                    eval_placeholder.markdown(eval_text + " ▌")
                eval_placeholder.markdown(eval_text)
            except Exception as e:
                st.error(f"Gemini API error during evaluation: {e}")
                
            # ── Step 3: Parse Winner & Build Graphviz Tree ───────────────
            winner = 1
            # Search for "Path X" in evaluation output. We pick the last mentioned one.
            matches = re.findall(r'Path (\d+)', eval_text, re.IGNORECASE)
            if matches:
                valid_matches = [int(m) for m in matches if 1 <= int(m) <= num_paths]
                if valid_matches:
                    winner = valid_matches[-1]
            
            # Show the winning path explicitly inside the Eval container
            st.success(f"### ✅ Selected Solution\\n**Path {winner}** was selected.\\n\\n{collected_paths[winner-1]}")
            st.success(f"### 🎯 Final Answer\\n{eval_text}")
            
            # Build Graphviz Digraph
            dot = graphviz.Digraph(comment='Reasoning Tree')
            dot.attr(rankdir='TB', size='10,10')
            
            def wrap_text(text, width=30):
                return "\\n".join(textwrap.wrap(str(text).replace('"', "'"), width=width))

            dot.node('Problem', 'Problem', shape='box')

            for i in range(num_paths):
                path_idx = i + 1
                is_winner = path_idx == winner
                
                node_name = f'Path {path_idx}'
                node_label = f'Path {path_idx}\\n{wrap_text(path_conclusions[i][:100] + "...")}'
                
                if is_winner:
                    node_label += '\\n(Selected)'
                    dot.node(node_name, node_label, shape='box', style='filled', fillcolor='lightgreen')
                else:
                    dot.node(node_name, node_label, shape='box')
                    
                dot.edge('Problem', node_name)
                dot.edge(node_name, 'Final Answer')
                
            dot.node('Final Answer', 'Final Answer', shape='box', style='filled', fillcolor='lightgreen')

            # Inject Graphviz Chart at the top placeholder
            with tree_placeholder.container():
                st.markdown("### 🌳 Reasoning Tree Visualization")
                st.graphviz_chart(dot)
                
            # ── Step 4: View Prompt Expander ─────────────────────────────────
            st.divider()
            with st.expander("View Prompt"):
                st.code(evaluator_prompt)
