import sqlite3
from jinja2 import Environment,FileSystemLoader

def fetch_books():
    conn = sqlite3.connect("book_prices.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * from book_info ORDER BY book_title")

    rows = cur.fetchall()

    conn.commit()
    conn.close()

    books=[]
    for row in rows:
        books.append({ "book_title" : row["book_title"],
                "book_price_num" : row["book_price_num"],
                "book_star_num" : row["book_star_num"],
                "book_stock" : row["book_stock"],
                "book_cover_img" : row["book_cover_img"],
                "scraped_at" : row["scraped_at"]})
        
    print(books)

fetch_books()
