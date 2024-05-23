from interface import CSSKWInterface
from _extractors import _KWExtractors, _CSSExtractors
from _utils import _Utils

URLS = ["https://archive.org/about"]

for URL in URLS:
    print(
        _Utils.generate_and_save_html_from_css_palette(
            URL, *_CSSExtractors.get_css_palette_url2colors_api(URL)
        )
    )
    # print(CSSKWInterface.get_css_kw_spacy(URL))
    # print(CSSKWInterface.get_css_kw_spacy_ranked(URL))
    # print(CSSKWInterface.get_css_kw_spacy_CHROME_INSTALLED(URL))
    # print(CSSKWInterface.get_css_kw_spacy_ranked_CHROME_INSTALLED(URL))
    pass
