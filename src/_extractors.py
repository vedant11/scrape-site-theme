# Importing necessary modules
import json
import re

import en_core_web_sm
import requests
import spacy
from src.config import url2colors_headers

from src._utils import _Utils

nlp = spacy.load("en_core_web_sm")


class _KWExtractors:
    def get_keywords_spacy_en_core_web_sm(url_txt) -> list:
        """
        not good enough
        ents:list = get_keywords_spacy_en_core_web_sm(url_txt)
        """
        nlp = en_core_web_sm.load()
        doc = nlp(url_txt)
        return [re.sub(r"\s+", " ", ent.text) for ent in doc.ents]


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
        return palette

    def get_css_palette_from_ss(URL) -> list:
        """
        palette:dict = get_css_palette_from_ss(pil_ss)
        clustered_palette = Helper._cluster_colors(palette)
        """
        pil_ss = _Utils.get_webpage_ss(URL)
        palette = _Utils.SSToPalette.generate(pil_ss)
        return palette
