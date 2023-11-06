from bs4 import BeautifulSoup
import requests
import re

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.find(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3").a['href'])
print(soup.find('h3').a['href'])

for link in soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
    product_link = main_url + link.a['href']
    print(product_link)
