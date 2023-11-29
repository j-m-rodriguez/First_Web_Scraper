from bs4 import BeautifulSoup
import requests
import csv
import re
import os

main_url = "https://books.toscrape.com/"
main_r = requests.get(main_url)
main_soup = BeautifulSoup(main_r.text, 'html.parser')

header = ['product_page_url', 'universal_product_code',
          'book_title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available',
          'product_description', 'category',
          'review_rating', 'image_url'
          ]
product_info = {}
# setting up directory for CSV files and images
absolute_path = os.path.dirname(__file__)
relative_path = "Rodriguez_Jonathan_2_data_images_112023"
full_path = os.path.join(absolute_path, relative_path)
if not os.path.exists(full_path):
    os.makedirs(full_path)
# contains all <li> elements with category and category book
category_links = main_soup.find(class_="nav nav-list").ul
# outer loop that goes through all categories
for link in category_links.find_all('a'):
    # obtain url for the category
    category_url = main_url + link['href']
    # obtain category name
    category = ' '.join(list(filter(None, re.split(r'\s|\\n', link.contents[0]))))
    product_info['category'] = category
    # csv file directory
    csv_dir = os.path.join(full_path, "data") + "\\"
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    # image file directory
    image_dir = os.path.join(full_path, "images", category) + "\\"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    r = requests.get(category_url)
    # soup of category page
    soup = BeautifulSoup(r.text.encode('latin1').decode('utf-8'), 'html.parser')

    # set up csv for each category
    csv_file = csv_dir + category + ".csv"
    f = open(csv_file, 'w', newline='')
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()

    # variable for image naming
    i = 0
    while True:
        # switched to class=product_pod
        for book in soup.find_all(class_="product_pod"):
            product_section = list(filter(None, re.split(r'\.\./', book.a['href'])))
            product_page_url = main_url + "catalogue/" + product_section[0]
            product_info['product_page_url'] = product_page_url
            product_info['book_title'] = book.img['alt']
            image_url = main_url + book.img['src']
            product_info['image_url'] = image_url

            r_product = requests.get(product_page_url)
            product_soup = BeautifulSoup(r_product.text.encode('latin1').decode('utf-8'), 'html.parser')
            # product info table
            product_values = product_soup.find_all('td')

            # product upc, prices, and quantity
            product_info['universal_product_code'] = product_values[0].contents[0]
            product_info['price_excluding_tax'] = product_values[2].contents[0]
            product_info['price_including_tax'] = product_values[3].contents[0]
            product_info['quantity_available'] = product_values[5].contents[0]
            # get product description
            product_info['product_description'] = product_soup.article.contents[7].contents[0]

            # locate review rating
            rating_location = product_soup.find(class_="star-rating")
            product_info['review_rating'] = rating_location['class'][1]

            # download all images
            img_data = requests.get(image_url).content
            with open(image_dir + 'image_' + str(i) + '.jpg', 'wb') as handler:
                handler.write(img_data)
            i += 1

            # write product information to csv file, use a different charset in case of error
            try:
                f = open(csv_file, 'a', newline='')
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writerow(product_info)
            except UnicodeEncodeError:
                f = open(csv_file, 'a', newline='', encoding='utf-16')
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writerow(product_info)

        # search for possible next page and create a new soup if there is
        # try:
        try:
            next_page = re.sub(r"[a-z]*?\.html", soup.find(class_="next").a['href'], category_url)
        except AttributeError:
            break
        r = requests.get(next_page)
        soup = BeautifulSoup(r.text.encode('latin1').decode('utf-8'), 'html.parser')
