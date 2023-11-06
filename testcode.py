from bs4 import BeautifulSoup
import requests
import re

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')
'''
# loops through each product by the class and retrieves product link
for link in soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
    product_page_url = main_url + link.a['href']
    print(product_page_url)
    r_product = requests.get(product_page_url)
    product_soup = BeautifulSoup(r_product.text, 'html.parser')
print(book_soup.find_all('td')[0].contents[0])
print(book_soup.find_all('td')[2].contents[0])
'''
book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
r_book = requests.get(book_url)
book_soup = BeautifulSoup(r_book.text, 'html.parser')

img_location = str((book_soup.find(class_="item active").contents[1]))
img = re.split(r'(media.*jpg)', img_location)
print(main_url + img[1])

for link in soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
    print(main_url + link.img['src'])
    print(link.img['alt'])
    product_page_url = main_url + link.a['href']
    print(product_page_url)