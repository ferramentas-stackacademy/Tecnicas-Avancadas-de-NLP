import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def getSummary(content):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em resumo de texto. Responda em português."},
            {"role": "user", "content": content}
        ]
    )
    
    return response['choices'][0]['message']['content']

def getAnswer(content, question):    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista que sabe responder perguntas com base no texto. Responda em português."},
            {"role": "assistant", "content": f'Com base no texto: "{content}". Responda as perguntas.'},
            {"role": "user", "content": question}
        ]
    )
    
    return response['choices'][0]['message']['content']    
