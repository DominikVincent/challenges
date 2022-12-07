import argparse
import io

import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import re
from pywebio.input import input, FLOAT, textarea, radio, actions
from pywebio.output import put_text, put_markdown, put_image, use_scope, put_button
from pywebio.session import set_env

import json

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
    soup = query_webpage('https://en.wikipedia.org/wiki/Special:Random')
    # soup = query_webpage('https://en.wikipedia.org/wiki/Asakent')
    # soup = query_webpage('https://en.wikipedia.org/wiki/Criollas_de_Caguas')
    # soup = query_webpage('https://en.wikipedia.org/wiki/Jean_Paul')

    title = soup.find('title').contents[0]
    source = json.dump(requests.get(f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={title}&rvslots=*&rvprop=content&formatversion=2&format=json"))
    return soup, source

def get_image(image_url: str):
    # Open the url image, set stream to True, this will return the stream content.
    query_url = "http:"+image_url
    print(query_url)
    r = requests.get(query_url, headers={'User-Agent' : "Magic Browser"})


    # Check if the image was retrieved successfully
    if r.status_code == 200:
        bytes_im = io.BytesIO(r.content)
        img_np = np.array(Image.open(bytes_im))
        # TODO fix svg.png images only having one channel when opening with PIL and not with cv2.
        print(img_np.shape)
        if img_np.shape[-1] != 3 and img_np.shape[-1] != 4 and img_np.shape[-1] != 1 and len(img_np.shape) != 2:
            print(f"Img is not 1, 3 or 4 channel returning None for {image_url}")
            return
        return img_np

    else:
        print('Image Couldn\'t be retreived')


"""
Expects lists of image urls. Then plots all images with their corresponding url text
"""
def show_images(images):
    if len(images) == 0:
        return
    fig, axs = plt.subplots(len(images))
    if not isinstance(axs, np.ndarray):
        axs = [axs]

    for image, ax in zip(images, axs):
        image_url = image["src"]
        ax.set_title(f"{image_url}\nalt: {image['alt']}")
        img = get_image(image_url)
        if img is not None:
            print(f"Image shape: {img.shape}")
            ax.imshow(img)
    plt.show()


def extract_images(soup):
    # Extract the image urls and alt texts and the corresponding location
    images = [{"src": img['src'], "alt": img['alt']} for img in soup.find_all('img')]

    # TODO consider removing duplicates. But what is a duplicate alt texts are context dependent so the same src file
    #  might have different alt texts in different contexts

    image_urls = []
    for img in images:
        test = re.findall(r'/(\d+)px-', img["src"])
        if len(test) == 1:
            image_size = int(test[0])
            if image_size > 0:
                image_urls.append(img)
            else:
                print(f"Sorting out image because it is too small {img}")
        else:
            print(f"Image does not contain pixel size. Sorting out: {img}")

    title = soup.find('title').contents[0]

    return image_urls, title


def update_wikitext_alt(wikitext, image_url, alt_text):
    # Search for image_url in wikitext and update the alt in the wiki
    image_name = re.findall(r'.*?/\d+px-(.*)', image_url)
    # TODO handle multiple ocurrences
    image_name = image_name[0].replace('_', ' ')

    # Now find the first occurance of the image name in the wikitext
    res = re.search(r".*?\[\[File:"+image_name+r"\s*\|(.*?)\]\]", wikitext, flags=re.IGNORECASE)
    if "alt" in res.group(0):
        # Handle replacement
        alt_pos = re.search(r".*?|\s*alt=.*?[\]\|]", wikitext, flags=re.IGNORECASE)

        pass
    else:
        # Add new alt element
        wikitext = wikitext[:res.end()-2] + f"|alt={alt_text}" + wikitext[res.end()-2:]

    return wikitext


def user_updates():
    set_env(title="Alt Text Tool")

    finished = False
    while not finished:
        soup, wikitext = random_webpage()

        images, title = extract_images(soup)
        print("title: ", title)
        with use_scope('wikipage', clear=True):
            put_markdown(f'# Alt Text Update Tool: {title}')

            for image in images:
                with use_scope("image", clear=True):
                    put_markdown('## Please add alt text')

                    put_image(image["src"])

                    if image["alt"] == "":
                        put_text("The image has no alt text please add it.")
                        text = input('Alt Text', rows=3, placeholder='Add the alt text here')
                        image["alt"] = text

                        wikitext = update_wikitext_alt(wikitext, image["src"], image["alt"])
                    else:
                        put_text(f"Current alt text is: '{image['alt']}'. Do you think that fits?")
                        answer = actions('Does the alt text fit?', [{"label":'Yes', "value": True, "color":"primary"},
                                                                    {"label":'No', "value": False, "color":"warning"}])
                        if not answer:
                            text = input('Suggest New Alt Text', rows=3, placeholder='Add the alt text here')
                            image["alt"] = text
                            wikitext = update_wikitext_alt(wikitext, image["src"], image["alt"])


            print(images)
            finished = actions("Current wiki page done. Do you want to fix another.", [{"label":'Yes', "value": False, "color":"primary"},
                                                                    {"label":'No', "value": True, "color":"warning"}])
            print("finished: ", finished)

    with use_scope('wikipage', clear=True):
        put_markdown(f'# Thank you! See you next time')


def main():

    soup = random_webpage()

    images, title = extract_images(soup)

    show_images(images)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # main()
    user_updates()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
