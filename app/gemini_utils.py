import google.generativeai as genai
import markdown  # << new import
from dotenv import load_dotenv

import os
load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # your key here

def get_expense_insights(expenses_data):
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"These are my recent expenses: {expenses_data}. Give me a short summary and smart insights, add recommendations to improve spending habits or expenses, spends are in INR. Do not add any extra greeting statements or follow up questions. Just give me the insights in markdown format. "

    response = model.generate_content(prompt)
    
    # Convert the markdown response text into HTML
    html_insights = markdown.markdown(response.text)
    
    return html_insights

