import streamlit as st
import google.generativeai as genai
import os 
import plotly.graph_objects as go
from dotenv import load_dotenv
load_dotenv()   # load env varibles 
from PIL import Image 
import json

import time

def interact_with_chatbot(prompt):
    # Generate a response from the chatbot model
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(prompt)
    return response.text

# Define Streamlit app
st.title("How may I help you?")

# Get user input
user_input = st.text_input("You: ")

if st.button("Send"):
    # Display user input
    if user_input.strip():
        st.text("You: " + user_input)

        # Get response from chatbot
        response = interact_with_chatbot(user_input)

        # Display chatbot response
        st.text(response)
    else:
        st.error("Please enter your text")