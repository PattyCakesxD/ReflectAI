import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ReflectAI", layout="centered")

st.markdown("""
            # :blue[ResumeAI]

            #### See your resume through a *:rainbow[critical eye]*
            """)

uploaded_file = st.file_uploader(":green[Upload your resume] :gray[(PDF)]", type=["pdf"])