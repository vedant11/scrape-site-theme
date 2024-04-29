# Importing necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import spacy
import time


def get_print_keywords(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(5)
    url_txt = driver.find_element(By.XPATH, "/html/body").text
    driver.close()
    nlp = spacy.load("en_core_sci_lg")
    doc = nlp(url_txt)
    print(url_txt)
    print(doc.ents)
