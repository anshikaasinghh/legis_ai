import streamlit as st
import google.generativeai as genai




import subprocess
subprocess.run(["pip", "install", "--upgrade", "google-generativeai"])


st.title("Test Google Generative AI")
genai.configure(api_key="xxx")
model = genai.GenerativeModel("gemini-1.5-flash")
st.write("Model loaded successfully!")
