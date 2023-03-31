# streamlit library
import streamlit as st

# HTML requests library
from requests_html import HTMLSession

# basic libraries
import matplotlib.pyplot as plt
import pandas as pd
import time
from PIL import Image

# enviroment variables libraries
import os
from dotenv import load_dotenv

# load enviroment variables from the .env file
load_dotenv()

# set the Site and the API url from the .env file
SITE_URL = os.getenv("SITE_URL")
API_URL = os.getenv("API_URL")

# set the route path
QUESTION_ROUTE = "answer" 
SUMMARY_ROUTE = "summary"

# start an HTML session to get page contents
sess = HTMLSession()

# call the server API routes to get an answer or a summary of a web page
def get_data(route, url, question):    
    api_url = f"{API_URL}/{route}?url={url}&question={question}"
    course_json = sess.get(api_url).text
    return course_json

# create the sidebar
with st.sidebar:
    add_radio = st.radio(
        "Escolha uma opção:",
        ("Responder perguntas sobre o Curso", "Resumir o conteúdo do Curso")
    )    

# check which radio button is selected
if add_radio == "Responder perguntas sobre o Curso":
    disabled = False
else:
    disabled = True

# insert images and fields on the interface
image = Image.open('./images/logo.jpg')
st.image(image, width=100)
st.title('Stack Academy')
st.title('Assistente de Cursos')
question = st.text_input("O que deseja saber?", "Do que se trata esse curso?", disabled=disabled)

# check if the Send button was pressed and get the API Data
if st.button("Enviar"):        
    with st.spinner('Mágica em andamento...'):
        if add_radio == "Responder perguntas sobre o Curso":
            answer = get_data(QUESTION_ROUTE, url=SITE_URL, question=question)
        else:
            answer = get_data(SUMMARY_ROUTE, url=SITE_URL, question=question)    

    # Print the API Response like it is being typed in real time
    st.markdown("## Resposta")
    st.markdown("---")
    text = answer
    t = st.empty()
    for i in range(len(text) + 1):
        t.markdown("## %s" % text[0:i])
        time.sleep(0.04)
