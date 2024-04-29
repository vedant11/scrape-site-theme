# Importing necessary modules
import json
import time

import en_core_web_sm
import numpy as np
import requests
import scipy.cluster
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import url2colors_headers


def get_print_keywords(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(5)
    url_txt = driver.find_element(By.XPATH, "/html/body").text
    driver.close()

    # not good enough
    nlp = en_core_web_sm.load()
    doc = nlp(url_txt)
    print("url_txt", url_txt, "\n")
    print("doc.ents", doc.ents, "\n")


def get_css_pallete(URL):
    """
    todo:
    1. extract image palletes as well
    """
    api_endpoint = "https://url2colors.com/api/colors"
    # post with the URL
    response = requests.post(
        api_endpoint,
        data=json.dumps({"prevUrl": URL.split("https://")[1]}),
        headers=url2colors_headers,
    )
    pallete = response.json()
    print("pallete for URL", URL, pallete)
    print("dominant colors", cluster_colors(pallete))


def cluster_colors(pallete: list):
    # Convert image to an array of RGB values
    ar = np.asarray(pallete)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

    # Perform K-means clustering
    codes, _ = scipy.cluster.vq.kmeans(ar, 4)

    # Assign codes to image pixels
    vecs, _ = scipy.cluster.vq.vq(ar, codes)

    # Count occurrences of each cluster
    counts, _ = scipy.histogram(vecs, len(codes))

    # Find the most frequent cluster (dominant color)
    index_max = scipy.argmax(counts)
    peak = codes[index_max]

    # Convert the dominant color to hexadecimal
    color = "#{:02x}{:02x}{:02x}".format(*map(int, peak))
    print(f"Most frequent color is {peak} ({color})")


def generate_html_from_css_pallete(*colors):
    """"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{colors[0]} and {colors[1]} Theme</title>
        <style>
            body {{
                background-color: {colors[1]};
                color: white;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                color: {colors[0]};
            }}
            p {{
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome to My Website!</h1>
        <p>This is a simple website using {colors[0]} and {colors[1]} colors.</p>
    </body>
    </html>
    """
    with open("generated_index.html", "w") as f:
        f.write(html)
