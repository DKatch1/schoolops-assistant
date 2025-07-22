import streamlit as st
from openai import OpenAI  # Make sure your OpenAI package is up to date

# --- CONFIG ---
st.set_page_config(page_title="SchoolOps Assistant", page_icon="🎓", layout="centered")

# --- PASSWORD GATE ---
PASSWORD = "allianceonly"
password = st.text_input("Enter access password:", type="password")
if password != PASSWORD:
    st.warning("Access restricted. Please enter the correct password.")
    st.stop()

# --- MAIN APP UI ---
st.title("🎓 SchoolOps Assistant")
st.write("Ask a question based on school attendance policies, procedures, and tools.")

# --- User Prompt ---
prompt = st.text_area("Your Question:", placeholder="e.g., When do I use the L0 code?", height=100)

if st.button("Get Answer") and prompt.strip():
    with st.spinner("Thinking..."):
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # Call GPT-4 Turbo
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a school operations assistant responding using Alliance's attendance policy documents only. Respond clearly and professionally."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.3
            )

            answer = response.choices[0].message.content
            st.markdown("### 📘 Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
