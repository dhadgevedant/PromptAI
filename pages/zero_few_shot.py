import streamlit as st
from utils.prompts import PAGE1_SAMPLES, get_zero_shot_prompt, get_few_shot_prompt
from utils.llm import generate_text

# Header Section
st.markdown('<h1 class="gradient-text">🎯 Zero & Few-Shot Prompting</h1>', unsafe_allow_html=True)
st.markdown("""
This page demonstrates the difference between **Zero-Shot Prompting** (giving instructions without examples) 
and **Few-Shot Prompting** (providing reference examples of the desired style and output).
""")

# Sample Click-to-Fill
st.markdown("### 📋 Sample Customer Emails")
cols = st.columns(len(PAGE1_SAMPLES))
for idx, (title, content) in enumerate(PAGE1_SAMPLES.items()):
    if cols[idx].button(f"📄 Load: {title}", use_container_width=True):
        st.session_state["p1_email"] = content

# Default text if session state is empty
default_email = st.session_state.get(
    "p1_email", 
    "Hi, I bought a camera from your store yesterday. It turns on but the screen is completely black. I want to return it immediately."
)

st.markdown("---")

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### ✍️ Customer Email Input")
    email_input = st.text_area("Edit the customer email:", value=default_email, height=150)
    
    prompt_mode = st.radio(
        "Select Prompting Technique:",
        options=["Zero-Shot", "Few-Shot"],
        help="Zero-shot requests a response directly. Few-shot feeds examples to guide response tone and format."
    )
    
    generate_btn = st.button("🚀 Generate Response", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("### 🔍 Model Output")
    
    if generate_btn:
        api_key = st.session_state.get("api_key")
        if not api_key:
            st.error("🔑 Please enter/load your Gemini API Key in the left sidebar configuration to proceed.")
        else:
            # Construct the prompt based on selection
            if prompt_mode == "Zero-Shot":
                prompt_to_send = get_zero_shot_prompt(email_input)
                sys_instruction = "You are a professional customer support executive. Reply politely."
            else:
                prompt_to_send = get_few_shot_prompt(email_input)
                sys_instruction = "You are a professional customer support executive. Reply politely."
            
            with st.spinner("Analyzing email and generating reply..."):
                try:
                    response_text = generate_text(
                        prompt=prompt_to_send,
                        api_key=api_key,
                        system_instruction=sys_instruction
                    )
                    
                    # Display response card
                    st.markdown("#### ✉️ Response Card")
                    st.markdown(f"""
                    <div class="response-card">
                        {response_text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display debugging prompt used
                    st.markdown("#### 📜 Prompt Sent to LLM")
                    st.markdown(f"""
                    <div class="prompt-card">{prompt_to_send}</div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error calling Gemini API: {e}")
    else:
        st.info("Input a customer email and click 'Generate Response' to see the difference between Zero-Shot and Few-Shot prompting styles.")
