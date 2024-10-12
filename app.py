import json
import openai
import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# The candidate_data_chat function
def cbic_chat(prompt, API_key):
    # Set OpenAI API key
    openai.api_key = API_key
    os.environ['OPENAI_API_KEY'] = API_key

    # Load embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

    # Load the vector store for the specific candidate
    vector_store_path = 'embeddings'
    vectorstore = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)

    # Create a retriever and LLM
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 12})
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        #model="gpt-4o",
        api_key=openai.api_key
    )

    # Create QA system
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Ask the question
    response = qa(prompt + ' Strictly answer based on the context. You must provide references')
    answer = response.get('result', '')  # Parse the result
    return answer

# Streamlit app layout
st.title("CBIC Chatbot")

user_prompt = st.text_area("Enter your question or prompt:")
api_key = st.text_input("Enter your OpenAI API Key:")

# Button to submit
if st.button("Ask the Chatbot"):
    if user_prompt and api_key:
        try:
            # Call the candidate data chat function
            result = cbic_chat(user_prompt, api_key)
            st.success("Chatbot Response:")
            st.write(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter all the required fields!")
