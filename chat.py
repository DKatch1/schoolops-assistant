import streamlit as st
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(page_title="SchoolOps Assistant (Chat)", page_icon="🎓", layout="centered")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- PASSWORD GATE ---
PASSWORD = "allianceonly"
if "authenticated" not in st.session_state:
    password = st.text_input("Enter access password:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
    else:
        st.warning("Access restricted. Please enter the correct password.")
        st.stop()

# --- INIT CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a school operations assistant responding using Alliance's attendance policy documents only. Respond clearly and professionally."}
    ]

# --- UI ---
st.title("🎓 SchoolOps Assistant")
st.write("Ask a question based on school attendance policies, procedures, and tools.")

for msg in st.session_state.messages[1:]:  # skip system prompt
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Prompt Input ---
if prompt := st.chat_input("Ask your SchoolOps question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=True,
        )
        response = ""
        placeholder = st.empty()
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            response += delta
            placeholder.markdown(response + "▌")
        placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
