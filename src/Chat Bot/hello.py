import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader #for pdf reading
import streamlit as st #streamlit to make the model more interactive for normal users
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFacePipeline
from langchain.callbacks import get_openai_callback

# Load .env having the huggingface key
load_dotenv()

# Global variables to store user information
user_info = {
    "name": "",
    "phone": "",
    "email": ""
}

# Spliting of the text into chunks 
def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # Converting the chunks of text into embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") #huggingface embedding with tranformers
    knowledgeBase = FAISS.from_texts(chunks, embeddings) #contains the chunks and embeddings
    
    return knowledgeBase

# Main program to read the pdf 
def main():
    st.title("Chat with your PDF 💬")
    
    pdf = st.file_uploader('Upload your PDF Document', type='pdf') #User's upload the pdf documents here
    
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        # Text variable will store the pdf text for every pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # knowledge base object
        knowledgeBase = process_text(text)
        
        # Insert queries to predict
        query = st.text_input('Ask a question related to the PDF ')
        cancel_button = st.button('Cancel')
        
        #cancel button to stop the search
        if cancel_button:
            st.stop()
        
        #queries
        if query:
            docs = knowledgeBase.similarity_search(query) # Performing the similarity search from the pdf provided
            #defining the LLM model to be used by the model
            llm = HuggingFacePipeline.from_model_id(model_id="google/flan-t5-large", task="text2text-generation", model_kwargs={"temperature": 0, "max_length": 200}, device=0) 
            chain = load_qa_chain(llm, chain_type='stuff') # Defining the chunks types
                
                # Returns the queries asked
            with get_openai_callback() as cost:
                response = chain.run(input_documents=do cs, question=query)
                print(cost)
              
                #generated responses    
            st.write(response)
    
if __name__ == "__main__":
    main()
