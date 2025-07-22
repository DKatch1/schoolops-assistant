import streamlit as st
from openai import OpenAI  # <-- NEW client

# --- CONFIG ---
st.set_page_config(page_title="SchoolOps Assistant", page_icon="🎓", layout="centered")

# --- PASSWORD GATE (simple) ---
PASSWORD = "allianceonly"
password = st.text_input("Enter access password:", type="password")
if password != PASSWORD:
    st.warning("Access restricted. Please enter the correct password.")
    st.stop()

# --- MAIN APP ---
st.title("🎓 SchoolOps Assistant")
st.write("Ask a question based on school attendance policies, procedures, and tools.")

# --- User input ---
prompt = st.text_area("Your Question:", placeholder="e.g., When do I use the L0 code?", height=100)

if st.button("Get Answer") and prompt:
    with st.spinner("Thinking..."):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])  # <-- NEW client instance
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # <-- THIS works with new client only
            messages=[
                {"role": "system", "content": "You are a school operations assistant responding using Alliance's attendance policy documents only."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.3
        )
        answer = response.choices[0].message.content
        st.markdown("### 📘 Answer")
        st.write(answer)

