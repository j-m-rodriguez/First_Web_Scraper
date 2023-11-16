from bs4 import BeautifulSoup
import requests
import csv
import re

main_url = "https://books.toscrape.com/"
main_r = requests.get(main_url)
main_soup = BeautifulSoup(main_r.text, 'html.parser')

header = ['product_page_url', 'universal_product_code',
          'book_title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available',
          'product_description', 'category',
          'review_rating', 'image_url'
          ]
# contains all <li> elements with category and category book
category_links = main_soup.find(class_="nav nav-list").ul
for link in category_links.find_all('a'):
    # obtain url for the category
    category_url = main_url + link['href']
    print(category_url)
    # obtain category name
    category = ' '.join(list(filter(None, re.split(r'\s|\\n', link.contents[0]))))
    print(category)
    r = requests.get(category_url)
    # soup of category page
    soup = BeautifulSoup(r.text.encode('latin1').decode('utf-8'), 'html.parser')

    # set up csv for each category
    csv_file = category + ".csv"
    f = open(csv_file, 'w', newline='')
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    while True:
        for book in soup.find_all(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
            product_section = list(filter(None, re.split(r'\.\./', book.a['href'])))
            product_page_url = main_url + "catalogue/" + product_section[0]
            print(product_page_url)
            book_title = book.img['alt']
            print(book_title)
            image_url = main_url + book.img['src']
            print(image_url)
            r_product = requests.get(product_page_url)
            product_soup = BeautifulSoup(r_product.text.encode('latin1').decode('utf-8'), 'html.parser')
            # product info table
            product_values = product_soup.find_all('td')
            print(product_values)

            # product upc, prices, and quantity
            universal_product_code = product_values[0].contents[0]
            print(universal_product_code)
            price_excluding_tax = product_values[2].contents[0]
            print(price_excluding_tax)
            price_including_tax = product_values[3].contents[0]
            print(price_including_tax)
            quantity_available = product_values[5].contents[0]
            print(quantity_available)
            # get product description
            product_description = product_soup.article.contents[7].contents[0]
            print(product_description)
            # get category by navigating down contents of <ul> tree
            '''
            # got category earlier
            category = product_soup.ul.contents[5].contents[1].contents[0]
            print(category)
            '''
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
            header_product = {header[i]: product[i] for i in range(len(header))}
            print(header_product)

            f = open(csv_file, 'a', newline='')
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writerow(header_product)
        try:
            next_page = re.sub(r"/.*?\.html", "/", category_url) + soup.find(class_="next").a['href']
            print(next_page)
            r = requests.get(next_page)
            soup_category = BeautifulSoup(r.text.encode('latin1').decode('utf-8'), 'html.parser')
        except Exception:
            break
