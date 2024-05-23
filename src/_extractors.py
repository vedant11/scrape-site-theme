# Importing necessary modules
import argparse
import json
import os
import re
import sys
import time
from collections import OrderedDict, namedtuple

import en_core_web_sm
import numpy as np
import requests
import scipy
import spacy
from _utils import _Utils
from bs4 import BeautifulSoup
from config import url2colors_headers
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.common.by import By
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")


class _KWExtractors:
    def get_keywords_spacy_en_core_web_sm(url_txt) -> list:
        """
        not good enough
        ents:list = get_keywords_spacy_en_core_web_sm(url_txt)
        """
        nlp = en_core_web_sm.load()
        doc = nlp(url_txt)
        print("url_txt", url_txt, "\n")
        print("doc.ents", doc.ents, "\n")
        return [ent.text for ent in doc.ents]


class _CSSExtractors:
    def get_css_palette_url2colors_api(URL) -> dict:
        """
        palette:dict = get_css_palette_url2colors_api("https://www.google.com")
        clustered_palette = Helper._cluster_colors(palette)
        """
        api_endpoint = "https://url2colors.com/api/colors"
        # post with the URL
        response = requests.post(
            api_endpoint,
            data=json.dumps({"prevUrl": URL.split("https://")[1]}),
            headers=url2colors_headers,
        )
        palette = response.json()
        print("palette for URL", URL, palette)
        return palette

    def get_css_palette_from_ss(URL) -> list:
        """
        palette:dict = get_css_palette_from_ss(pil_ss)
        clustered_palette = Helper._cluster_colors(palette)
        """
        pil_ss = _Utils.get_webpage_ss(URL)
        palette = _Utils.SSToPalette.generate(pil_ss)
        return palette
