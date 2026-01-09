import pdfkit
import os

def html_to_pdf(html_path,pdf_path):
    options = {
        "header-center" : "Heheheee : Scraped at [time] : [date]",
        "header-font-size": "10",

        "footer-right": "Page [page] of [topage]",
        "footer-font-size": "7",

        "page-size" : "A4", 
        "margin-top": "20mm",
        "margin-bottom": "20mm",
        "margin-left": "15mm",
        "margin-right": "15mm",
        "enable-local-file-access":""
        }
    config = pdfkit.configuration(wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" )
    pdfkit.from_file(html_path,pdf_path,options=options,configuration=config)
    print("Newsletter PDF generated: output/books_newsletter.pdf")


html_path = "output/books_newsletter.html"
pdf_path = "output/books_newsletter.pdf"

print("HTML exists", os.path.exists(html_path))
html_to_pdf(html_path, pdf_path)
