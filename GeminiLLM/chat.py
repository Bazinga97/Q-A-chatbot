import requests
import streamlit as st
from streamlit_lottie import st_lottie
import os
import google.generativeai as genai
from dotenv import load_dotenv
from random import choice

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    """
    Sends the user's question to the Generative AI model and returns the response.
    """
    response = chat.send_message(question, stream=True)
    return response

# Function to load Lottie animation
def load_lottieurl(url):
    """
    Loads a Lottie animation from the given URL.
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function to generate dynamic suggestions
def generate_suggestions(user_input):
    """
    Generates dynamic suggestions based on the user's input.
    """
    suggestions = [
        f"{user_input} for beginners",
        f"Best practices for {user_input}",
        f"How to learn {user_input}",
        f"Resources to master {user_input}",
        f"Tips and tricks for {user_input}"
    ]
    return suggestions

# List of quotes
quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Believe you can and you're halfway there. - Theodore Roosevelt",
    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill"
]

# Streamlit app configuration
st.set_page_config(page_title="Chat_bot", page_icon="🤖", layout="wide")

# Load animation
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")

# App header
col1, col2 = st.columns([1, 3])
with col1:
    st_lottie(lottie_coding, height=200, key="coding")
with col2:
    st.title("🤖 Chat_bot")

# Instructions
st.write("## 💬 Instructions")
st.write("Welcome to the Chat_bot! You can ask me anything, and I'll do my best to provide a helpful response. Simply type your question in the input field below and click the 'Ask' button.")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Chat interface
st.write("## 💬 Chat Interface")
input_container = st.container()
with input_container:
    user_input = st.text_input("Input: ", key="input", placeholder="Ask me anything...")
    submit = st.button("Ask")

if submit:
    if user_input.strip():
        # Show loading indicator
        with st.spinner("Processing your question..."):
            response = get_gemini_response(user_input)
        st.session_state['chat_history'].append(("You", user_input))
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))
    else:
        st.warning("Please enter a valid question.")

# Chat history
if st.session_state['chat_history']:
    st.write("## 📜 Chat History")
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: black;'><strong>{role}:</strong> {text}</div>", unsafe_allow_html=True)
        else:
            quote = choice(quotes)
            st.markdown(f"<div style='background-color: #e0e0e0; padding: 10px; border-radius: 10px; margin-bottom: 10px; color: black;'><strong>{role}:</strong> {text}<br><small>{quote}</small></div>", unsafe_allow_html=True)

# Suggestions
st.write("## 💡 Suggestions")
if user_input:
    suggestions = generate_suggestions(user_input)
else:
    suggestions = [
        "How can I improve my coding skills?",
        "What are the latest trends in machine learning?",
        "Can you explain the concept of natural language processing?",
        "How can I optimize my website for better performance?",
        "What are some best practices for cybersecurity?"
    ]

for suggestion in suggestions:
    st.markdown(f"- {suggestion}")

# Footer
st.write("---")
st.write("Made with :heart: by Nilesh Kumar")
st.write("### Stay Connected")
st.write("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/your_username)")
st.write("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/your_username/)")
st.write("[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/your_username)")
