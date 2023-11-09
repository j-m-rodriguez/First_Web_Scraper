from bs4 import BeautifulSoup
import requests
import re
import csv

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

first_category = soup.find(class_="nav nav-list").ul.a['href']
category_link = main_url + first_category
print(category_link)
r_category = requests.get(category_link)
soup_category = BeautifulSoup(r_category.text, 'html.parser')
# headers for CSV file
header = ['product_page_url', 'universal_product_code',
          'book_title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available',
          'product_description', 'category',
          'review_rating', 'image_url'
          ]
# open CSV file and write headers
f = open('single_category.csv', 'w')
for each in header:
    f.write(each + ",")
f.write('\n')
f.close()
while True:
    for link in soup_category.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        product_section = list(filter(None, re.split(r'\.\./', link.a['href'])))
        product_page_url = main_url + "catalogue/" + product_section[0]
        print(product_page_url)
        book_title = link.img['alt']
        book_title = re.sub(r"â\S+", "'", book_title)
        print(book_title)
        image_url = main_url + link.img['src']
        print(image_url)
        r_product = requests.get(product_page_url)
        product_soup = BeautifulSoup(r_product.text, 'html.parser')
    # string of product info
        product_table = str(product_soup.find_all('td'))
    # list of product info
        product_values = re.split(r',| |\(|\)|\[|]|Â|<.+?>', product_table)
        product_values = list(filter(None, product_values))
        print(product_values)
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
        product_description = re.sub("â..", r"'", product_description)
        print(product_description)
    # get category by navigating down contents of <ul> tree
        category = product_soup.ul.contents[5].contents[1].contents[0]
        print(category)
    # locate and print review rating
        rating_location = product_soup.find(class_="star-rating")
        review_rating = rating_location['class'][1]
        print(review_rating)
    # create list of all product details
        product = list()
        product.append(product_page_url)
        product.append(universal_product_code)
        product.append(book_title)
        product.append(price_including_tax)
        product.append(price_excluding_tax)
        product.append(quantity_available)
        product.append(product_description)
        product.append(category)
        product.append(review_rating)
        product.append(image_url)
        print(product)
    # dictionary of everything
        header_product = {}
        i = 0
        for each in header:
            header_product[each] = product[i]
            i += 1
        print(header_product)
        csv_file = open('single_category.csv', 'a', newline='')
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writerow(header_product)
    try:
        next_page = re.sub(r"/.*?\.html", "/", category_link) + soup_category.find(class_="next").a['href']
        print(next_page)
        r = requests.get(next_page)
        soup_category = BeautifulSoup(r.text, 'html.parser')
    except Exception:
        break
csv_file.close()
