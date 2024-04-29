# Importing necessary modules
import json
import time

import en_core_web_sm
import requests
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
    1. extract image pallete
    """
    api_endpoint = "https://url2colors.com/api/colors"
    # post with the URL
    response = requests.post(
        api_endpoint,
        data=json.dumps({"prevUrl": URL.split("https://")[1]}),
        headers=url2colors_headers,
    )
    print("pallete for URL", URL, response.json())
