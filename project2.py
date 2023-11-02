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
print(fb_link)

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
#print(product_table)

# list of product info
product_values = re.split(r',| |\(|\)|\[|]|Â|<.+?>', product_table)
product_values = list(filter(None, product_values))
print(product_values)

# product upc, prices, and quantity
universal_product_code = product_values[0]
print(universal_product_code)
price_excluding_tax = product_values[2]
print(price_excluding_tax)
price_including_tax = product_values[3]
print(price_including_tax)
quantity_available = product_values[7]
print(quantity_available)

# trying to get description from 'meta'
'''
print(book_soup.find_all('meta'))
print('line 54')
for line in book_soup.find_all('meta'):
    print(line)
print(book_soup.find('meta').string)
'''
# get product description from class="product_page"
for child in book_soup.find_all('p', class_="product_page").children:
    print(child)
#    print(child)
#    if child.string is None or len(child.string) < 25:
#        continue
#    else:
#        product_description = child.string
#print(product_description)
#another way to find product description
des = book_soup.find(class_="product_page").find_all('p')[3]
print(des)
# path to description
#/html/body/div/div/div[2]/div[2]/article/p
product_description2 = book_soup.article.contents[7].contents[0]
print(product_description2)

# get category by navigating down contents of <ul> tree
category = book_soup.ul.contents[5].contents[1].contents[0]
print(category)

# locate and print review rating
rating_location = book_soup.find(class_="star-rating")
review_rating = rating_location['class'][1]
print(review_rating)

img_location = str((book_soup.find(class_="item active").contents[1]))
img = re.split(r'(media.*jpg)', img_location)
print(main_url + img[1])