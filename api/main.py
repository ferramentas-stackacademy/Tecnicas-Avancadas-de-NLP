from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import httpx
from bs4 import BeautifulSoup
from services import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8501",
    "https://8501-giuferreira-cursotecnic-cew0gqba5so.ws-us92.gitpod.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def getContent(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    content = ' '.join(paragraphs)    
    return content

@app.get("/", response_class=PlainTextResponse)
async def root():
    return "API GPT is Alive"

@app.get("/summary", response_class=PlainTextResponse)
async def summary(url: str):
    content = await getContent(url)
    summary = openai.getSummary(content)
    return summary

@app.get("/answer", response_class=PlainTextResponse)
async def answer(url: str, question: str):
    content = await getContent(url)
    answer = openai.getAnswer(content, question)
    return answer
