from bs4 import BeautifulSoup
import requests
import re

main_url = "https://books.toscrape.com/catalogue/category/books_1/"
first_page = main_url + "index.html"
r = requests.get(first_page)
soup = BeautifulSoup(r.text, 'html.parser')

while True:
    # loops through each product by the class and retrieves product link, title, and img url,
    for link in soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        product_page_url = main_url + link.a['href']
        print(product_page_url)
        book_title = link.img['alt']
        print(book_title)
        image_url = main_url + link.img['src']
        print(image_url)
        r_product = requests.get(product_page_url)
        product_soup = BeautifulSoup(r_product.text, 'html.parser')
    '''
# string of product info
        product_table = str(product_soup.find_all('td'))
# list of product info
        product_values = re.split(r',| |\(|\)|\[|]|Â|<.+?>', product_table)
        product_values = list(filter(None, product_values))
# product upc, prices, and quantity
        universal_product_code = product_values[0]
        print(universal_product_code)
        price_including_tax = product_values[3]
        print(price_including_tax)
        price_excluding_tax = product_values[2]
        print(price_excluding_tax)
        quantity_available = product_values[7]
        print(quantity_available)
# get product description
        product_description = product_soup.article.contents[7].contents[0]
        print(product_description)
# get category by navigating down contents of <ul> tree
        category = product_soup.ul.contents[5].contents[1].contents[0]
        print(category)
# locate and print review rating
        rating_location = product_soup.find(class_="star-rating")
        review_rating = rating_location['class'][1]
        print(review_rating)
'''
    try:
        next_page = main_url + soup.find(class_="next").a['href']
        print(next_page)
        r = requests.get(next_page)
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        break
print('done')