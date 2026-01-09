from google import genai
import os
from newsletter_html import books

def prompt_maker():
    return f"""
    You are being given some data about a book.
    Title: {books[0]['book_title']}
    Price: £{books[0]['book_price_num']}
    Rating: {books[0]['book_star_num']} out of 5
    Stock: {books[0]['book_stock']}
    Scraped at: {books[0]['scraped_at']}

    Write a concise, neutral summary. You can also give a brief about what the book is about by searching the title of the book
    """


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_maker())

print(response.text)
