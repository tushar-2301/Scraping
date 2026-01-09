import sqlite3
from jinja2 import Environment,FileSystemLoader

def fetch_books():
    conn = sqlite3.connect("book_prices.db")
    conn.row_factory = sqlite3.Row          # a very imp line because if we dont give it this line then rows=list(tuples) but now we are telling to set each row as Row datatype itself, it comes with sqlite and its a diff type of datatype and data from it can be accessed like a dict also and by indexing as well
    cur = conn.cursor()                     # changing the datatype to row basically would cause better access to the data since now we dont have to write row[0][1]
    
    cur.execute("SELECT * from book_info ORDER BY book_title")

    rows = cur.fetchall()

    conn.close()

    books=[]            # providing the jinja2 template by a list of dict is a standard practice since it is the most convenient to access data
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
    template = env.get_template("book_newsletter.txt")

    context = {
        "books" : books
    }

    output = template.render(context)
    return output

def save_output(text, filename="output/books_newsletter.txt"):
    import os
    os.makedirs("output",exist_ok=True)
    
    with open (filename, "w", encoding="utf-8") as f:
        f.write(text)

books = fetch_books()
print("Fetched %s from DB" % len(books))

text = render_newsletter(books)
save_output(text)

print("Newsletter generated: output/books_newsletter.txt")
