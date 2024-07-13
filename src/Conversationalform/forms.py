import openai
import streamlit as st
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Replace with GEMINI API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
openai.api_key = GEMINI_API_KEY

# Define the JSON file path
JSON_FILE_PATH = 'user_information.json'

def save_user_information(name, phone, email):
    # Load existing data
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []

    # Add new user information
    new_user = {
        "name": name,
        "phone": phone,
        "email": email
    }
    data.append(new_user)

    # Save updated data back to the JSON file
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

# Gets users informations
def get_user_information():
    st.title("Chatbot")

    #Generates response
    def generate_response(prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def chatbot(prompt):
        with st.spinner("Chatbot is typing..."):
            response = generate_response(prompt)
        return response

    #
    st.subheader("Welcome to our service!")
    user_question = st.text_input("How can I assist you today?")

    if "call" in user_question.lower():
        st.write("Sure, I can arrange a call for you. I just need some information.")
        
        name = st.text_input("What's your name?")
        phone = st.text_input("What's your phone number?")
        email = st.text_input("What's your email address?")
        
        if st.button("Submit"):
            if name and phone and email:
                save_user_information(name, phone, email)
                st.write("Thank you! Our team will contact you soon.")
            else:
                st.write("Please provide all the information.")

if __name__ == "__main__":
    get_user_information()
