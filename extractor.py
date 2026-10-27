# importing the required python packages

import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
import re



URL = "https://books.toscrape.com/catalogue/page-{}.html"

# writing a header inorder to prevent the website from blocking the scraper thinking it is malicious
HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

books = [ ]

print("Starting the initialisation of the 50 pages...........")

# Iterating over the 50 web pages
for page in range(1 , 51) :

    #creating a unique url for every page iteration
    url = URL.format(page)

    # Using exceptions to try to get the data and also to handle errors
    try :
        print(f"Getting response from {url}.......")
        response = requests.get(url , headers=HEADERS)

        # Doing confirmations on the status code to make sure it is the correct one 
        if response.status_code != 200 :
            print(f"Page {page} not scraped to avoid breaking code. Status code : {response.status_code}")
            continue

    except Exception as e :
        print("Sorry! A network error has occured ")
        continue

    else :
        print(f"Scraping data from page {page} of 50")
        #parsing the html content 
        soup = BeautifulSoup(response.text , "html.parser")

        #filtering all the books 
        Books = soup.find_all("article" , class_="product_pod")

        #Iterating over the Books
        for book in Books :

            # Getting the book's name
            book_name = book.h3.a["href"]

            # Getting the price of the book
            b = book.find("div" , class_="product_price")
            book_price = b.p.text

            # cleaning the data 
            book_name = book_name.replace("/index.html" , "")
            book_price = float(re.sub(r"[^\d\.]" , "" , book_price))

            # creating a dict object for the book and it's price
            d = {
                "Title" : book_name,
                "Price" : book_price
            }

            # Adding the dict object to a huge list
            books.append(d)

    # Pausing the program for 5 seconds before moving to scrape the next page.
    time.sleep( 5 )


# using conditionals to check whether data has been collected
if len(books) == 0 :
    print("Data not collected")

else :
    # creating a pandas Dataframe object out of the data collected
    df = pd.DataFrame(books)

    # converting the dataframe to a csv file which can be stored in the system's storage
    df.to_csv("Books.csv" , index=False)

    print("successfuly created the csv")