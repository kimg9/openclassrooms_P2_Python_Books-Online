import requests
import os
import wget 

from bs4 import BeautifulSoup

def product_parsing(website, product_page_url):
    #--------------------------------- GET PAGE -------------------------------------------
    response = requests.get(product_page_url)
    if response.status_code != 200:
        print('\nERROR: Could not fetch product page')
        exit(1)

    soup = BeautifulSoup(response.content, 'html.parser')
    #--------------------------------------------------------------------------------------


    #--------------------------------- PARSING --------------------------------------------
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()

    product = soup.find('article', {'class': 'product_page'})

    title = product.findChild("h1").text.strip()
    image_url = website + (product.find('div', {'class': 'item active'}).findChild('img', recursive=False)['src'][6:])
    image_extension = os.path.splitext(image_url)[1]

    # RETREAVING IMAGE --------------------------------------------------------------------
    path = (f"media/{category.upper().replace(' ', '_')}/")
    directory_exists = os.path.exists(path)
    if not directory_exists:
        os.makedirs(path)

    print(f"\nIMAGE: downloading image for book {title}...")
    for ch in ['\\','`','*','/','{','}','[',']','(',')','>','#','+','-','.','!','?','$','\'',',',' ','!',':']:
        if ch in title:
            title = title.lower().replace(ch, '_')
    
    image_path = path + category.upper().replace(' ', '_') + "_" + title
    file_exists = os.path.exists(image_path)
    if file_exists:
        os.remove(image_path)
    wget.download(image_url, out = (image_path + image_extension))
    #-------------

    try:
        product_description = product.findChild('p', recursive=False).text
    except AttributeError:
        product_description = ""

    product_info = product.findChild('table', recursive=False).find_all('td')
    upc = product_info[0].text
    price_without_tax = product_info[2].text
    price_with_tax = product_info[3].text
    number_available = "".join(_ for _ in product_info[5].text if _ in "0123456789")

    review_rating = product.find('div', {'class': 'row'}).find('div', {'class': 'product_main'}).findChildren('p', recursive=False)[2]['class']
    if "One" in review_rating:
        review_rating = "1"
    elif "Two" in review_rating:
        review_rating = "2"
    elif "Three" in review_rating:
        review_rating = "3"
    elif "Four" in review_rating:
        review_rating = "4"
    elif "Five" in review_rating:
        review_rating = "5"
    #--------------------------------------------------------------------------------------


    #--------------------------------- RETURN PARSED DATA ---------------------------------
    data = [product_page_url, upc, title, price_with_tax, price_without_tax, number_available, product_description, category, review_rating, image_url]

    return data
    #--------------------------------------------------------------------------------------


