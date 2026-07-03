"""
Page 2 – Structured Reasoning Simulator
Uses: Gemini Flash Lite (gemini-1.5-flash-8b) with real-time streaming.
"""

import streamlit as st
import re
import graphviz
import textwrap
from utils.prompts import PAGE2_SAMPLES, get_cot_prompt
from utils.llm import generate_stream

# ── Header ──────────────────────────────────────────────────────────────────
st.title("🧠 Structured Reasoning Simulator")
st.markdown(
    "This page demonstrates **step-by-step reasoning** powered by **Gemini Flash Lite**. "
    "The model thinks out loud — breaking the problem into steps before giving a final answer."
)

with st.expander("💡 What is Chain of Thought?"):
    st.markdown(
        """
**Chain of Thought (CoT)** prompting encourages a language model to produce
intermediate reasoning steps rather than jumping straight to an answer.

Instead of asking *"What is the answer?"*, we prompt the model to:

1. **Understand** what the problem is asking.
2. **Break it down** into smaller pieces.
3. **Work through** each piece explicitly.
4. **Verify** its work.
5. **State** the final answer.

This technique dramatically improves accuracy on math, logic, and multi-step problems
because it forces the model to "show its work".
"""
    )

st.divider()

# ── Sample quick-fill buttons ────────────────────────────────────────────────
st.markdown("**📋 Sample Questions** — click to load one")
cols = st.columns(len(PAGE2_SAMPLES))
for idx, (title, content) in enumerate(PAGE2_SAMPLES.items()):
    if cols[idx].button(title, use_container_width=True, key=f"p2_sample_{idx}"):
        st.session_state["p2_question"] = content

# ── Input ────────────────────────────────────────────────────────────────────
default_q = st.session_state.get(
    "p2_question",
    "If a farmer has 20 chickens and buys 15 more, then sells 10, how many remain?"
)
question_input = st.text_input(
    "Enter your math or logic problem:",
    value=default_q,
    placeholder="e.g. A train travels 60 km in 1 hour. How long to travel 150 km?"
)

solve_btn = st.button("🧠 Solve — Think Out Loud", type="primary", use_container_width=True)

# ── Output ───────────────────────────────────────────────────────────────────
if solve_btn:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.error("🔑 Please enter your Gemini API Key in the sidebar to continue.")
    elif not question_input.strip():
        st.warning("Please enter a problem first.")
    else:
        prompt = get_cot_prompt(question_input)

        st.divider()
        st.markdown("### Reasoning")
        st.caption(
            "⚠️ These are generated reasoning traces from a language model and not the model's private internal chain of thought."
        )

        placeholder = st.empty()
        accumulated = ""
        try:
            for chunk in generate_stream(prompt, api_key):
                accumulated += chunk
                placeholder.markdown(accumulated + " ▌")
            placeholder.markdown(accumulated)   # remove cursor
            
            # ── Flow Diagram Visualization ──────────────────────────────────────
            st.divider()
            st.markdown("### 📊 Reasoning Flow Diagram")
            
            lines = accumulated.split('\n')
            steps = []
            current_step = ""
            final_answer = ""
            
            for line in lines:
                line_str = line.strip()
                if re.match(r'^(Step \d+|[1-9]\.|-|\*)\s', line_str, re.IGNORECASE):
                    if current_step:
                        steps.append(current_step.strip())
                    current_step = line_str
                elif "final answer" in line_str.lower() or "answer:" in line_str.lower():
                    if current_step:
                        steps.append(current_step.strip())
                        current_step = ""
                    final_answer += line_str + "\n"
                else:
                    if current_step:
                        current_step += " " + line_str
                    elif final_answer:
                        final_answer += " " + line_str

            if current_step:
                steps.append(current_step.strip())

            # Fallback: split by paragraph
            if not steps:
                paragraphs = [p.strip() for p in accumulated.split('\n\n') if p.strip()]
                if len(paragraphs) > 1:
                    steps, final_answer = paragraphs[:-1], paragraphs[-1]
                else:
                    steps, final_answer = paragraphs, "See reasoning above."

            if not final_answer.strip():
                final_answer = steps.pop() if steps else "Could not parse final answer."

            # Render Graphviz Flowchart
            dot = graphviz.Digraph(comment='Flow Diagram')
            dot.attr(rankdir='TB', size='8,8')
            
            def wrap_text(text, width=45):
                return "\\n".join(textwrap.wrap(str(text).replace('"', "'"), width=width))
                
            dot.node('Problem', 'Problem', shape='box')
            prev_node = 'Problem'
            
            for i, step in enumerate(steps):
                node_name = f'Step {i+1}'
                node_label = f'Step {i+1}\\n{wrap_text(step[:150] + "..." if len(step) > 150 else step)}'
                dot.node(node_name, node_label, shape='box')
                dot.edge(prev_node, node_name)
                prev_node = node_name
                
            dot.node('Final Answer', f'Final Answer', shape='box', style='filled', fillcolor='lightgreen')
            dot.edge(prev_node, 'Final Answer')
            
            st.graphviz_chart(dot)

            # Final Answer Success card
            st.success(f"🎯 **Final Answer**\\n\\n{final_answer}")

            # ── View Prompt ──────────────────────────────────────────────────────
            st.divider()
            with st.expander("View Prompt"):
                st.code(prompt)

        except Exception as e:
            st.error(f"Gemini API error: {e}")
