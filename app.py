import streamlit as st
import pandas as pd
import ollama

# Page settings
st.set_page_config(
    page_title="Data Detective AI | Mazen Faraj",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Custom CSS for a clean look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .footer { 
        position: fixed; left: 0; bottom: 0; width: 100%; 
        color: #6c757d; text-align: center; font-size: 12px; 
        padding: 10px; background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown("<h1 style='text-align: center;'>🕵️‍♂️ Data Detective AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px;'>Welcome to the investigation system by <b>Mazen Faraj</b></p>", unsafe_allow_html=True)
st.divider()

# Layout columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📁 Upload Data")
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
        st.write("### Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

with col2:
    st.subheader("💬 Investigation Chat")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": "Hello! I am your AI assistant. **Developed by Mazen Faraj**. Upload a file and let's start!"
            }
        ]

    # Show messages
    chat_box = st.container(height=400)
    with chat_box:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    # Chat input
    if user_input := st.chat_input("Ask me about the data..."):
        if not uploaded_file:
            st.warning("Please upload a file first!")
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with chat_box:
                with st.chat_message("user"):
                    st.markdown(user_input)

                # Prepare context for Gemma
                preview = df.head(15).to_string()
                prompt = f"You are a forensic expert. Dev by: Mazen Faraj. Data: {preview}\nUser Question: {user_input}"

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing..."):
                        # Call local gemma model
                        res = ollama.generate(model='gemma3:4b', prompt=prompt)
                        msg = res['response']
                        st.markdown(msg)
                        st.session_state.messages.append({"role": "assistant", "content": msg})

# Footer info
st.markdown("""
    <div class="footer">
        Data Detective AI: Forensic analysis tool powered by Gemma 3. <br>
        Developed by: <b>Mazen Faraj</b>
    </div>
    """, unsafe_allow_html=True)