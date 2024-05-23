# Importing necessary modules
from collections import namedtuple

import spacy
from src._utils import _Utils

from src._extractors import _CSSExtractors, _KWExtractors

nlp = spacy.load("en_core_web_sm")

CSSKW = namedtuple("CSSKW", ["css", "kw"])


class CSSKWInterface:
    @staticmethod
    def get_fastest_way_css_kw(URL) -> CSSKW:
        """
        Dependencies:
        url: bs
        kw : spacy
        css: url2colors API

        Usage:
        keywords:list = get_fastest_way_css_kw("https://www.google.com")
        """
        url_txt = _Utils.get_url_txt_bs(URL)
        kw = _KWExtractors.get_keywords_spacy_en_core_web_sm(url_txt)
        css = _CSSExtractors.get_css_palette_url2colors_api(URL)
        return CSSKW(css, kw)

    @staticmethod
    def get_css_kw_spacy(URL) -> CSSKW:
        """
        Dependencies:
        url: bs
        kw : spacy
        css: url2colors API

        Usage:
        keywords:list = get_css_kw_spacy_bs("https://www.google.com")
        """
        url_txt = _Utils.get_url_txt_bs(URL)
        kw = _KWExtractors.get_keywords_spacy_en_core_web_sm(url_txt)
        css = _CSSExtractors.get_css_palette_url2colors_api(URL)
        return CSSKW(css, kw)

    @staticmethod
    def get_css_kw_spacy_ranked(URL) -> CSSKW:
        """
        Dependencies:
        url: bs
        kw : spacy
        css: url2colors API

        keywords:list = get_css_kw_spacy_ranked("https://www.google.com")
        """
        url_txt = _Utils.get_url_txt_bs(URL)
        tr4w = _Utils.SpacyTextRank4Keyword()
        tr4w.analyze(
            url_txt, candidate_pos=["NOUN", "PROPN"], window_size=4, lower=False
        )
        kw = tr4w.get_keywords(10)
        css = _CSSExtractors.get_css_palette_url2colors_api(URL)
        return CSSKW(css, kw)

    @staticmethod
    def get_css_kw_spacy_CHROME_INSTALLED(URL) -> CSSKW:
        """
        Dependencies:
        url: Selenium
        kw : spacy
        css: url2colors API

        Usage:
        keywords:list = get_css_kw_spacy_bs("https://www.google.com")
        """
        url_txt = _Utils.get_url_txt_slnm(URL)
        # url_txt = _Utils.get_page_source(URL)
        kw = _KWExtractors.get_keywords_spacy_en_core_web_sm(url_txt)
        css = _CSSExtractors.get_css_palette_from_ss(URL)
        return CSSKW(css, kw)

    @staticmethod
    def get_css_kw_spacy_ranked_CHROME_INSTALLED(URL) -> CSSKW:
        """
        Dependencies:
        url: Selenium
        kw : spacy
        css: url2colors API

        keywords:list = get_css_kw_spacy_ranked("https://www.google.com")
        """
        url_txt = _Utils.get_url_txt_slnm(URL)
        # url_txt = _Utils.get_page_source(URL)
        tr4w = _Utils.SpacyTextRank4Keyword()
        tr4w.analyze(
            url_txt, candidate_pos=["NOUN", "PROPN"], window_size=4, lower=False
        )
        kw = tr4w.get_keywords(10)
        css = _CSSExtractors.get_css_palette_from_ss(URL)
        return CSSKW(css, kw)
