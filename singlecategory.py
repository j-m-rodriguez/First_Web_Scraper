from bs4 import BeautifulSoup
import requests
import re
import csv

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

first_category = soup.find(class_="nav nav-list").ul.a['href']
print(first_category)
category_link = main_url + first_category
print(category_link)
r_category = requests.get(category_link)
soup_category = BeautifulSoup(r_category.text.encode('latin1').decode('utf-8'), 'html.parser')
# headers for CSV file
header = ['product_page_url', 'universal_product_code',
          'book_title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available',
          'product_description', 'category',
          'review_rating', 'image_url'
          ]
product_info = {}
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
        product_info['product_page_url'] = product_page_url
        product_info['book_title'] = link.img['alt']
        image_url = main_url + link.img['src']
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
    # get category by navigating down contents of <ul> tree
        product_info['category'] = product_soup.ul.contents[5].contents[1].contents[0]
    # locate and print review rating
        rating_location = product_soup.find(class_="star-rating")
        product_info['review_rating'] = rating_location['class'][1]

        csv_file = open('single_category.csv', 'a', newline='')
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writerow(product_info)
    try:
        next_page = re.sub(r"/.*?\.html", "/", category_link) + soup_category.find(class_="next").a['href']
        print(next_page)
        r = requests.get(next_page)
        soup_category = BeautifulSoup(r.text.encode('latin1').decode('utf-8'), 'html.parser')
    except Exception:
        break

