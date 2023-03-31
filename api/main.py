# fastapi libraries
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

# web scrapping libraries
import httpx
from bs4 import BeautifulSoup

# service created to abstract the openai library functionalities
from services import openai

# Instantiate the API
app = FastAPI()

# Decide who can access te API
origins = [
    "http://localhost",
    "http://localhost:8501",
    "https://8501-giuferreira-cursotecnic-cew0gqba5so.ws-us92.gitpod.io", # Substitua pela url da sua aplicacao Streamlit (No gitpod está na aba Ports)
]

# Insert the access permissions in the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# function to web scrapping a page and return the content
async def getContent(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    content = ' '.join(paragraphs)    
    return content

# Check if the API is Alive
@app.get("/", response_class=PlainTextResponse)
async def root():
    return "API GPT is Alive"

# Return a Summary of a Web Page
@app.get("/summary", response_class=PlainTextResponse)
async def summary(url: str):
    content = await getContent(url)
    summary = openai.getSummary(content)
    return summary

# Return an Answer for a Question, based on the content oh the Web Page
@app.get("/answer", response_class=PlainTextResponse)
async def answer(url: str, question: str):
    content = await getContent(url)
    answer = openai.getAnswer(content, question)
    return answer
