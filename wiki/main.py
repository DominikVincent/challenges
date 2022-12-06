import argparse
import io

import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re

"""
Queries webpage and returns it

@:param - url from webpage
"""


def query_webpage(webpage: str) -> str:
    # Query a random Wikipedia page
    page = requests.get(webpage)

    print(page.url)

    # Parse the HTML
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def random_webpage():
    # soup = query_webpage('https://en.wikipedia.org/wiki/Special:Random')
    soup = query_webpage('https://en.wikipedia.org/wiki/Jean_Paul')
    return soup

def has_image() -> bool:
    pass

def get_image(image_url: str):
    # Open the url image, set stream to True, this will return the stream content.
    query_url = "http:"+image_url
    print(query_url)
    r = requests.get(query_url, headers={'User-Agent' : "Magic Browser"})


    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        bytes_im = io.BytesIO(r.content)
        img_np = np.array(Image.open(bytes_im))
        print(img_np.shape)
        if img_np.shape[-1] != 3:
            return
        return img_np

    else:
        print('Image Couldn\'t be retreived')


"""
Expects lists of image urls. Then plots all images with their corresponding url text
"""
def show_images(images):
    fig, axs = plt.subplots(len(images))
    for image_url, ax in zip(images, axs):
        img = get_image(image_url)
        if img is not None:
            ax.imshow(img)
            ax.set_title(image_url)
    plt.show()


def extract_images(soup):
    # Extract the images
    # divs = [div for div in soup.find_all('div', {'class': 'thumb tright'})],
    # images = [img['src'] for img in divs.find_all('img')]
    images = [img['src'] for img in soup.find_all('img')]

    #['/250px-']
    image_urls = []
    for img in images:
        matches = re.findall(r'/\d+px-', img)
        if len(matches) == 1:
            match = matches[0]
            image_size = int(match[1:-3])
            if image_size > 100:
                image_urls.append(img)

    title = soup.find('title')

    return image_urls, title

def extract_all_images(page_soup):
    img_tags = page_soup.find_all('img')
    urls = [img['src'] for img in img_tags]

    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if not filename:
            print("Regex didn't match with the url: {}".format(url))
            continue
        with open(filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)

def main():

    soup = random_webpage()

    images, title = extract_images(soup)

    show_images(images)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
