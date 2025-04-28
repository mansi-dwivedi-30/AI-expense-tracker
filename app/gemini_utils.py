import google.generativeai as genai
import markdown
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_expense_insights(expenses_data):
    # Check if there are enough entries
    if len(expenses_data) < 5:
        return "<p><em>Not enough entries to analyze spending habits yet. Add more expenses!</em></p>"

    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""These are my recent expenses: {expenses_data}.
    Give me a short summary and smart insights, add recommendations to improve spending habits or expenses.
    Spends are in INR. Do not add any extra greeting statements or follow-up questions.
    Just give me the insights in markdown format."""

    response = model.generate_content(prompt)

    # Convert the markdown response text into HTML
    html_insights = markdown.markdown(response.text)
    
    return html_insights
