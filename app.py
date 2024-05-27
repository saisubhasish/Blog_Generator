import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from langserve import add_routes
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title="Blogs creator",
    version='1.0',
    description='Blog creation using OpenAI'
)

model=ChatOpenAI()
prompt=ChatPromptTemplate.from_template("Write me a blog about {topic} with 100 words.")

add_routes(
    app,
    prompt|model,
    path='/blog'
)

if __name__=='__main__':
    uvicorn.run(app, host='localhost', port=8000)
