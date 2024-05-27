import requests
import streamlit as st


def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/blog/invoke", json={'input': {'topic': input_text}})

    return response.json()['output']['content']

st.title('Blog Generator')
input_text = st.text_input('Write an blog on')

if input_text:
    st.write(get_openai_response(input_text))