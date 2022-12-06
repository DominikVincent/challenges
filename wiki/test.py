import cv2
import io

import requests
import numpy as np
from PIL import Image
import re

def get_image():
    r = requests.get("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/RichterJP.jpg/250px-RichterJP.jpg", headers={'User-Agent' : "Magic Browser"})

    print("Request: ", r)
    print("Content: ", r.content)

    bytes_im = io.BytesIO(r.content)

    img = Image.open(bytes_im)

    img_np = np.array(img)
    print(img_np.shape)
    cv_im = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    print(cv_im)

    import matplotlib.pyplot as plt

    plt.imshow(cv_im)
    plt.show()

l = re.findall(r'/\d+px-', "http://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/RichterJP.jpg/250px-RichterJP.jpg")
print(l)
