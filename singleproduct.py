from bs4 import BeautifulSoup
import requests
import csv

main_url = "https://books.toscrape.com/"
r = requests.get(main_url)
soup = BeautifulSoup(r.text, 'html.parser')

product_link = soup.find(class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

# string of the location of the book
book_link = str(product_link.find("h3"))
print(book_link)

# list containing the product book
fb_list = book_link.split('"')
# print(fb_list)

# variable of product url
product_page_url = main_url + fb_list[1]
print(product_page_url)

# variable of product title
book_title = fb_list[3]
print(book_title)

# soup of the first product
r_book = requests.get(product_page_url)
book_soup = BeautifulSoup(r_book.text.encode('latin1').decode('utf-8'), 'html.parser')

# another method to get product info (change first index to match list item, however this doesn't take care of the 'Â'
product_values = book_soup.find_all('td')
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
product_description = book_soup.article.contents[7].contents[0]
print(product_description)

# get category by navigating down contents of <ul> tree
category = book_soup.ul.contents[5].contents[1].contents[0]
print(category)

# locate and print review rating
rating_location = book_soup.find(class_="star-rating")
review_rating = rating_location['class'][1]
print(review_rating)

img_location = str((book_soup.find(class_="item active").contents[1]))
img = re.split(r'(media.*jpg)', img_location)
image_url = main_url + img[1]
print(image_url)

product = []
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

header = ['product_page_url', 'universal_product_code',
          'book_title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available',
          'product_description', 'category',
          'review_rating', 'image_url'
          ]
header_product = {}
i = 0
for each in header:
    header_product[each] = product[i]
    i += 1
print(header_product)

with open('single_product.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header)
    writer.writeheader()
    writer.writerow(header_product)
