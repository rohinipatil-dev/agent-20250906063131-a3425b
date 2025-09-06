import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Streamlit page configuration
st.set_page_config(page_title="Programmer JokeBot", page_icon="🧠", layout="centered")

# Sidebar controls
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Model", options=["gpt-4", "gpt-3.5-turbo"], index=0)
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.8, 0.05)
st.sidebar.write("Set your OPENAI_API_KEY as an environment variable before running.")

st.title("🧠💻 Programmer JokeBot")
st.caption("A chatbot that tells clean, clever programming jokes. Ask for a theme, language, or topic!")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a witty, friendly comedian who specializes in programming humor. "
                "Rules:\n"
                "- Focus on clean, inclusive, and clever programming jokes (no offensive content).\n"
                "- Keep replies concise: usually 1–2 jokes per message, with very brief punchy explanations when helpful.\n"
                "- Vary formats (one-liners, Q&A, tiny snippets) and reference common dev life, bugs, version control, and languages.\n"
                "- If user requests a topic (e.g., Python, Git, regex), tailor jokes accordingly.\n"
                "- If the user asks for non-programming jokes, gently steer back to programming themes."
            ),
        }
    ]

def get_openai_response(history, model_name, temp):
    response = client.chat.completions.create(
        model=model_name,  # "gpt-4" or "gpt-3.5-turbo"
        messages=history,
        temperature=temp,
    )
    return response.choices[0].message.content

# Display chat history (skip system message)
for msg in st.session_state.messages:
    if msg["role"] in ("user", "assistant"):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask me for a programming joke (e.g., Python, Git, regex, AI, debugging)...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Loading a punchline..."):
            try:
                reply = get_openai_response(st.session_state.messages, model, temperature)
            except Exception as e:
                reply = "Oops! I hit a runtime error fetching that joke. Try again in a moment."
        st.markdown(reply)
    # Append assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Quick prompts
st.write("")
st.subheader("Try a quick topic")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Python"):
        st.session_state.messages.append({"role": "user", "content": "Tell me a Python joke."})
        reply = get_openai_response(st.session_state.messages, model, temperature)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.experimental_rerun()
with col2:
    if st.button("Git"):
        st.session_state.messages.append({"role": "user", "content": "Tell me a Git joke."})
        reply = get_openai_response(st.session_state.messages, model, temperature)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.experimental_rerun()
with col3:
    if st.button("Regex"):
        st.session_state.messages.append({"role": "user", "content": "Tell me a regex joke."})
        reply = get_openai_response(st.session_state.messages, model, temperature)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.experimental_rerun()