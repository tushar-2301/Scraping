import sqlite3
from jinja2 import Environment,FileSystemLoader


def fetch_books():
    conn = sqlite3.connect("book_prices.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * from book_info ORDER BY book_title")

    rows = cur.fetchall()

    conn.close()

    books=[]
    for row in rows:
        books.append({ "book_title" : row["book_title"],
                "book_price_num" : row["book_price_num"],
                "book_star_num" : row["book_star_num"],
                "book_stock" : row["book_stock"],
                "book_cover_img" : row["book_cover_img"],
                "scraped_at" : row["scraped_at"]})
        
    return(books)
    

def render_newsletter(books):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("book_newsletter.html")

    context = {
        "books" : books
    }

    output = template.render(context)
    return output


def save_output_as_html(text, filename="output/books_newsletter.html"):
    import os
    os.makedirs("output",exist_ok=True)
    
    with open (filename, "w", encoding="utf-8") as f:
        f.write(text)


html_path = "output/books_newsletter.html"


books = fetch_books()
print("Fetched %s from DB" % len(books))

text = render_newsletter(books)
save_output_as_html(text)
