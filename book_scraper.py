from playwright.sync_api import sync_playwright
import sqlite3
from urllib.parse import urljoin
from datetime import datetime

rating_map = { "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
base_url = "https://books.toscrape.com"


def scrape_page():

    book_list = []  #It is a list of tuples and will contain a tuple for each book containing all the details of the book
    total_books = page.locator("article.product_pod")  # #basically total_books is just a locator, it is not returning a list of all of the matching items it found, it just locates them

    book_count = total_books.count()

    for i in range(book_count):

        book_pod = total_books.nth(i) #now i am going through all the matched items found in total_books

        book_title = book_pod.locator("h3 a").get_attribute("title")
        
        book_price_str = book_pod.locator(".price_color").inner_text()
        book_price_num = float(book_price_str.replace("£", ""))

        #extracting info from the class attr 
        book_class = book_pod.locator("p.star-rating").get_attribute("class") 
        book_star_alpha = book_class.replace("star-rating ", "")
        book_star_num = rating_map[book_star_alpha]

        book_stock = book_pod.locator(".availability").get_attribute("class").replace(" availability", "")

        rel_image_url = book_pod.locator("img").get_attribute("src")
        book_cover_img = urljoin(base_url,rel_image_url)

        scraped_at = datetime.now().isoformat()

        book_pod_tuple = (book_title, book_price_num, book_star_num, book_stock, book_cover_img, scraped_at)

        book_list.append(book_pod_tuple)

    return book_list


def insert_values(book_list):

    cur.execute("""CREATE TABLE IF NOT EXISTS book_info (
                book_title TEXT UNIQUE NOT NULL,
                book_price_num REAL,
                book_star_num INTEGER,
                book_stock TEXT,
                book_cover_img TEXT,
                scraped_at TEXT
    ) """)
    
    cur.executemany("""INSERT INTO book_info 
                    (book_title, book_price_num, book_star_num, book_stock, book_cover_img, scraped_at) 
                    VALUES (?,?,?,?,?,?)
                    ON CONFLICT (book_title)
                    DO UPDATE SET
                    book_price_num = excluded.book_price_num,
                    book_star_num = excluded.book_star_num,
                    book_stock = excluded.book_stock,
                    book_cover_img = excluded.book_cover_img,
                    scraped_at = excluded.scraped_at 
                    """, book_list)
    
    #above is an UPSERT = INSERT + UPDATE function which basically would update the record whenever scraped again
    
def verify_db():
    conn = sqlite3.connect("book_prices.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM book_info")

    count = cur.fetchone()[0]
    print(count)

    # cur.execute("SELECT * FROM book_info")

    # rows = cur.fetchall()
    # for i in rows:
    #     print(i)

    conn.close()


conn = sqlite3.connect("book_prices.db")
cur = conn.cursor()
  
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://books.toscrape.com")


    while (True):
        # book_list = scrape_page()
        # insert_values(book_list)
        
        next_btn = page.locator("li.next a") # even if the next btn is not found locator will never give an error, .locator doesnt fetch you the details, it is only used when u do something about it (eg. click it) and thats when it would give an error

        if next_btn.count() == 0:    #its the same .count func that we had used above to find out the no of books on a page and if its 0 means no next btn exists
            print("No more pages exist, all pages succesfully scraped !!")
            break
        else:
            next_btn.click()
            page.wait_for_load_state("networkidle")  #networkidle is a condn that the browser page is not loading anything for 500ms and we are waiting for this state to be achieved after which w can move ahead 
            # waiting for loading is very imp, without it stops working abruptly somewhere ie if the page didnt load properly it wont find the next btn and hence it will terminate the loop

    browser.close()

conn.commit()
conn.close()

verify_db()




