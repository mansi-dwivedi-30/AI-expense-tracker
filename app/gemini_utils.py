import google.generativeai as genai

genai.configure(api_key="AIzaSyAA1qqAEr2DAiDQfQFcbxjrhs6dzK6BU4w")  # Replace with your actual key

def get_expense_insights(expenses_data):
    model = genai.GenerativeModel("gemini-2.0-flash")  # Keep using gemini-pro

    prompt = f"These are my recent expenses: {expenses_data}. Give me a short summary and smart insights."

    response = model.generate_content(prompt)
    return response.text
