import streamlit as st
from openai import OpenAI
from huggingface_hub import InferenceClient
import re
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
def looks_incompleate(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t=text.strip()
    if t.endswith(('.', '!', '?', ':', ';', '...', '"', "'")):
        return True
    if re.search(r'\d+\.\s*\*\*$', t):
        return True
    if re.search(r'[.!?]\s*$', t):
        return True
    return False
def complete_response(question: str, generate_response,role, max_retries=3) -> str:
    base_prompt = f"suppose you are {role},answer the question: {question}"
    answer = generate_response(base_prompt, temperature=0.3, max_tokens=1024)
    retries = 0
    while retries < max_retries and looks_incompleate(answer):
        continue_prompt = f"As a {role}, the previous answer seems incomplete. Please complete it seamlessly: {answer}"
        more_answer = generate_response(continue_prompt, temperature=0.3, max_tokens=1024)
        
        if not more_answer or more_answer.strip() in answer:
            break
        answer += " " + more_answer.strip()
        retries += 1
        
    return answer

def main():
    st.title("Question Answering AI")
    st.write("Welcome to the AI! Ask any question and get a detailed answer.")
    
    st.write("Choose a model:")
    choice = st.radio("Pick your favorite:", ["GROQ(relaible)", "HF(fast)"])
    if choice == "GROQ(relaible)":
        generate_response = groq
    else:
        generate_response = hf
        
    user_question = st.text_input("Enter your question:")
    if user_question:
        role=st.radio("pick a role:",["teacher","expert"])
        with st.spinner("Generating answer..."):
            response = complete_response(user_question, generate_response,role)
        st.write("### Answer:")
        st.markdown(response)
    else: 
        st.info("Please enter a question to get started.")
if __name__ == "__main__":
    main()