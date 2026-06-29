import streamlit as st
from openai import OpenAI
from huggingface_hub import InferenceClient
import io
import keys
GROQ_URL = "https://api.groq.com/openai/v1"
def hf(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    models = getattr(keys, "HF_MODEL", ["meta-llama/Llama-3.1-8B-Instruct"])
    key = getattr(keys, "hf_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'hf_key' variable in the keys module.")
    last_error = None
    for m in models:
        try:
            c = InferenceClient(token=key)
            r = c.chat_completions(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
            
    return f"HF model failed. Models tried: {models}. Error: {last_error}"
def groq(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    models = getattr(keys, "GROQ_MODEL", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    key = getattr(keys, "g_key", None)
    if key is None:
        raise ValueError("API key not found. Please set the 'g_key' variable in the keys module.")
    
    c = OpenAI(api_key=key, base_url=GROQ_URL)
    last_error = None
    for m in models:
        try:
            r = c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return r.choices[0].message.content
        except Exception as e:
            last_error = e
            continue
    return f"Groq model failed. Models tried: {models}. Error: {last_error}"
css = """
<style>
:root {
    color-scheme: light dark;
}
[data-testid="stSidebar"] {
    background-color: light-dark(#f8f9fa, #1f2937);
}
.history-wrap {
    max-height: 65vh; 
    overflow-y: auto; 
    padding-right: 4px;
}
.qa-card {
    border: 1px solid light-dark(#e2e8f0, #374151);
    background: light-dark(#ffffff, #111827);
    border-radius: 8px;
    padding: 12px;
    margin: 12px 0;
    box-shadow: 0 1px 3px light-dark(rgba(0,0,0,0.05), rgba(0,0,0,0.3));
}
.q {
    font-weight: 600; 
    color: light-dark(#1e3a8a, #93c5fd); 
    margin-bottom: 6px;
    font-size: 0.9rem;
}
.a {
    white-space: pre-wrap; 
    color: light-dark(#4a5568, #d1d5db); 
    line-height: 1.4;
    font-size: 0.85rem;
}
</style>
"""
def export_b(his):
    text = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(his, 1)])
    return io.BytesIO(text.encode('utf-8'))
def setup_ui():
    st.set_page_config(page_title="AI Teaching Assistant", layout="wide")
    st.markdown(css, unsafe_allow_html=True)
    st.session_state.setdefault("history", [])
    with st.sidebar:
        st.title("Settings & History")
        provider = st.selectbox("Choose AI Engine:", ["Groq", "Hugging Face"])
        st.write("---")
        col_cle, col_exp = st.columns(2)
        with col_cle:
            if st.button("Clear Chat", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        with col_exp:
            if st.session_state.history:
                st.download_button(
                    label="Export",
                    data=export_b(st.session_state.history),
                    file_name="conversation.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        st.write("---")
        cords = []
        for i,h in enumerate(st.session_state.history,1):
            cords.append(f'<div class="qa-card"><div class="q"> Q{i}: {h["question"]}</div> <div class="a"> {h["answer"]}</div></div>')
        st.markdown('<div class="history-wrap">' + "".join(cords) + "</div>", unsafe_allow_html=True)
    st.title("AI Teaching Assistant")
    st.write(f"Ask me anything! Powered currently by **{provider}**")
    with st.form("input_form", clear_on_submit=True):
        u = st.text_input("Enter your question:")
        submitted = st.form_submit_button("Ask Assistant", type="primary")
    if submitted:
        q = u.strip()
        if q:
            with st.spinner(f"Generating response using {provider}..."):
                try:
                    if provider == "Groq":
                        a = groq(q)
                        
                    else:
                        a = hf(q)
                except Exception as e:
                    a = f"An error occurred: {str(e)}"
            st.session_state.history.insert(0, {"question": q, "answer": a, "engine": provider})
            st.rerun()
        else:
            st.warning("Please type a question first.")
if __name__ == "__main__":
    setup_ui()