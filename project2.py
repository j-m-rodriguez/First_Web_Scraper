from bs4 import BeautifulSoup
import requests
import re

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

first_book = soup.find(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
# prints the html of the first product
# for child in first_book.children:
#    print(child)

# string of the element with the book link
fb_link = str(first_book.find("h3"))
# print(fb_link)

# list of the element with book link
fb_list = fb_link.split('"')
# print(fb_list)

# variable of product url
product_page_url = "https://books.toscrape.com/" + fb_list[1]
print(product_page_url)

# variable of product title
book_title = fb_list[3]
print(book_title)

# soup of the first product
r_book = requests.get(product_page_url)
book_soup = BeautifulSoup(r_book.text, 'html.parser')

# string of product info
product_table = str(book_soup.find_all('td'))
print(product_table)
print(type(product_table))

# list of product info
product_values = re.split('<.+?>',product_table)
print(product_values)
print(len(product_values))

# product upc, prices, and quantity
universal_product_code = product_values[1]
print(universal_product_code)
price_excluding_tax = product_values[5]
print(price_excluding_tax)
price_including_tax = product_values[7]
print(price_including_tax)
quantity_available = product_values[11]
print(quantity_available)
