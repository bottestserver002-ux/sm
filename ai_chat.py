import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = "AIzaSyBXTyYBOlIYgZz9s0BYTOKe8d2dbzTJ-g8"


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(message):
    response = model.generate_content(message)
    return response.text