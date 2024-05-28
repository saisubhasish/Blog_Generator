import requests
import streamlit as st

from utils.logger import logging
from utils.exception import BlogException

def get_openai_response(topic_name, tone, domain, number_of_words, type_of_blog):
    try:
        logging.info("'main': Post request to the backend API with given data")
        response = requests.post(
            "http://localhost:8000/blog",
            json={
                'topic_name': topic_name,
                'tone': tone,
                'domain': domain,
                'number_of_words': number_of_words,
                'type_of_blog': type_of_blog
            }
        )
        logging.info(f"'main': Request response: {response}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

st.title('Blog Generator')

with st.form("my_form"):
    st.write("Fill the input fields below: ")
    topic_name = st.text_input('Enter the topic name')
    tone = st.text_input('Blog writing tone (Casual/Informative/Formal/Humorous/Inspirational/Friendly/Curious/Pessimistic and optimistic)', value='Casual')
    domain = st.text_input('Domain')
    number_of_words = st.number_input('Number of words', min_value=1000, step=50)
    type_of_blog = st.text_input('Content type for audience (Beginner/Advanced)')
    logging.info(f"'main': Topic name: {topic_name}, Tone: {tone}, Domain: {domain}, Number of words: {number_of_words}, Type of blog: {type_of_blog}")

    submitted = st.form_submit_button("Submit")
    if submitted:
        logging.info("'main': Data submitted, now invoking the Backend API")
        response = eval(get_openai_response(topic_name, tone, domain, number_of_words, type_of_blog))
        logging.info(f"'main': Generated response: {response}")
        if 'error' in response:
            st.error(f"Error: {response['error']}")
        else:
            st.write("Title: ",response['blog']['title'])
            st.write(response['blog']['content'])

st.write("Thank you for using the blog generator.")