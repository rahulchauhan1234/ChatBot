import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFacePipeline
from langchain.callbacks import get_openai_callback

# Load environment variables if you have other keys as well
load_dotenv()

def process_text(text):
    # Split the text into chunks using Langchain's CharacterTextSplitter
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Convert the chunks of text into embeddings to form a knowledge base
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    knowledgeBase = FAISS.from_texts(chunks, embeddings)
    
    return knowledgeBase

def get_user_information():
    st.subheader("Please provide your information for a callback")
    
    name = st.text_input("What's your name?")
    phone = st.text_input("What's your phone number?")
    email = st.text_input("What's your email address?")
    
    if st.button("Submit"):
        if name and phone and email:
            st.write("Thank you! Our team will contact you soon.")
            # You can save the data to a database or send an email notification here.
        else:
            st.write("Please provide all the information.")    

def main():
    st.title("Chat with your PDF 💬")
    
    pdf = st.file_uploader('Upload your PDF Document', type='pdf')
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        # Text variable will store the pdf text
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Create the knowledge base object
        knowledgeBase = process_text(text)
        
        # Inserting questions to the system
        query = st.text_input('Ask a question to the PDF or type "call me" to request a call back')
        cancel_button = st.button('Cancel')
        
        if cancel_button:
            st.stop()
        
        if query:
            if "call me" in query.lower():
                get_user_information()
            else:
                docs = knowledgeBase.similarity_search(query) # Performing the similarity search
                llm = HuggingFacePipeline.from_model_id(model_id="google/flan-t5-large", task="text2text-generation", model_kwargs={"temperature": 0, "max_length": 200}, device=0)
                chain = load_qa_chain(llm, chain_type='stuff') # Defining the chunks types
                
                with get_openai_callback() as cost:
                    response = chain.run(input_documents=docs, question=query)
                    print(cost)
                    
                st.write(response)
    
if __name__ == "__main__":
    main()
