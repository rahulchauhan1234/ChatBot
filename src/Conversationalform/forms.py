import openai
import streamlit as st
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

# Load .env having the gemini api key
load_dotenv()

# Retrieve the gemini api key from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

#genai configurations with gemini api key
genai.configure(api_key=GEMINI_API_KEY)

# Defining the JSON file path
JSON_FILE_PATH = 'user_information.json'

#For user information
def save_user_information(name, phone, email):

    # Add new user information
    new_user = {
        "name": name,
        "phone": phone,
        "email": email
    }
    # Save updated data back to the JSON file
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(new_user, file, indent=4)

#Loading the user informations
def load_user_information():
    # Load existing data
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        data = []

    return data    

# Gets users information
def get_user_information():
    st.title("Conversational Form")

    # Generate response
    def generate_response(prompt):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        print(response.text)
        return response.text

    def chatbot(prompt):
        with st.spinner("Chatbot is typing..."):
            response = generate_response(prompt)
        return response
    
    # Header
    st.subheader("Welcome to our service!")
    #Input text area
    user_question = st.text_input("How can I assist you today?")

    # Call the form to fill by the users
    if "call" in user_question.lower():
        st.write("Sure, I can arrange a call for you. I just need some information.")
        
        name = st.text_input("What's your name?")
        phone = st.text_input("What's your phone number?")
        email = st.text_input("What's your email address?")
        
        #When submit button is clicked
        if st.button("Submit"):
            if name and phone and email:
                save_user_information(name, phone, email)
                st.write("Thank you! Our team will contact you soon.")
            else:
                st.write("Please provide all the information.")

    #Response when users ask the questions about their informations stored in the forms            
    else:
        if user_question:
            prompt = f''' You are an expert at question-answering. Below is the provided data for the context:
                        user_query = {user_question}\
                        json_data = {load_user_information()}\
                        Please retrieve the information from json_data that match the user_query and dont answer any other unnecessary things.'''
            
            with st.spinner("Chatbot is typing..."):
                response = generate_response(prompt)
            st.write(response)

if __name__ == "__main__":
    get_user_information()
