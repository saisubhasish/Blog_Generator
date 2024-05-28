import os
import sys
import json
import uvicorn
from openai import OpenAI
from langchain import hub
from dotenv import load_dotenv
from langserve import add_routes
from fastapi import FastAPI, Request
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from fastapi.responses import JSONResponse
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools import ArxivQueryRun
from langchain.agents import create_openai_tools_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper

from utils.prompts import *
from utils.logger import logging
from utils.exception import BlogException
from utils.utils import content_generation

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

app = FastAPI(
    title='Langchain Server',
    version='1.0',
    description='A simple API server'
)

def blog_content(topic_name, tone_of_the_blog_professional_casual_formal_friendly, domain, number_of_words, type_of_blog_beginner_or_advanced, grammar_error_in_major_minor_zero):
    try:
        model=ChatOpenAI()
        api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_contain_chars_max=500)
        wiki=WikipediaQueryRun(api_wrapper=api_wrapper)
        arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_contain_chars_max=500)
        arxiv=ArxivQueryRun(arxiv_wrapper=arxiv_wrapper)
        tools = [wiki, arxiv]
        llm = ChatOpenAI(model="gpt-4-0125-preview", temperature=0)
        prompt=hub.pull("hwchase17/openai-functions-agent")
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

        logging.info("'app': Getting the context from topic_name")
        response = agent_executor.invoke({'input': DESCRIPTION_EXTRACTION_SYSTEM_TEMPLATE.format(topic_name=topic_name)})
        context = response['output']
        logging.info("'app': Getting the catchy blog_title from topic_name")
        res0 = json.loads(content_generation(client,TITLE_GENERATION_SYSTEM_TEMPLATE.format(topic_name=topic_name), TITLE_GENERATION_USER_TEMPLATE))
        blog_title = res0['blog_title']
        logging.info("'app': Getting the format and keywords from blog_title")
        res1 = json.loads(content_generation(client,FORMAT_KEYWORD_GENERATION_SYSTEM_TEMPLATE.format(blog_title=blog_title), FORMAT_KEYWORD_GENERATION_USER_TEMPLATE))
        format = res1['format']
        keywords = res1['keywords']
        logging.info("'app': Generating the blog content")
        res2 = content_generation(client,
            BLOG_GENERATION_SYSTEM_TEMPLATE.format(
                context=context,
                tone_of_the_blog_professional_casual_formal_friendly=tone_of_the_blog_professional_casual_formal_friendly,
                blog_title=blog_title,
                domain=domain,
                format_of_the_blog=format,
                keywords=keywords,
                number_of_words=number_of_words,
                type_of_blog_beginner_or_advanced=type_of_blog_beginner_or_advanced,
                grammar_error_in_major_minor_zero=grammar_error_in_major_minor_zero,
            ),
            BLOG_GENERATION_USER_TEMPLATE
        )
        return res2
    except Exception as e:
        raise BlogException(e,sys)

@app.post('/blog')
async def blog(request: Request):
    try:
        logging.info(f"'app': Got data in request body: {request}")
        data = await request.json()
        logging.info(f"'app': Data: {data}")
        topic_name = data.get('topic_name')
        tone = data.get('tone')
        domain = data.get('domain')
        number_of_words = data.get('number_of_words')
        type_of_blog = data.get('type_of_blog')

        logging.info("'app': Function call to blog_content generation")
        response = blog_content(topic_name=topic_name, tone_of_the_blog_professional_casual_formal_friendly=tone, domain=domain, 
        number_of_words=number_of_words, type_of_blog_beginner_or_advanced=type_of_blog, grammar_error_in_major_minor_zero='minor')
        logging.info(f"'app': Function call response: {response}")
        return JSONResponse(content=response)

    except Exception as e:
        raise BlogException(e,sys)

if __name__=='__main__':
    logging.info("'app': Starting app")
    uvicorn.run(app,host='localhost',port=8000)

