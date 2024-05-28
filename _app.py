import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from langserve import add_routes
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title="Langchain Server",
    version='1.0',
    description='A simple API server'
)

model=ChatOpenAI()
prompt1=ChatPromptTemplate.from_template("Write me a blog about {topic} with 100 words.")

add_routes(
    app,
    prompt1|model,
    path='/blog'
)

if __name__=='__main__':
    uvicorn.run(app,host='localhost',port=8000)

