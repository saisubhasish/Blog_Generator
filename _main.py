import requests
import streamlit as st

def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/blog/invoke", json={'input': {'topic': input_text}})
    return response.json()['output']['content']

st.title('Blog Generator')
input_text = st.text_input('Enter the topic name')

if input_text:
    st.write(get_openai_response(input_text))


# topic_name
# tone_of_the_blog_professional_casual_formal_friendly
# domain
# number_of_words
# type_of_blog_beginner_or_advanced
# grammar_error_in_major_minor_zero