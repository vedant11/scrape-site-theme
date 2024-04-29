from script import get_print_keywords, get_css_pallete

URLs = [
    "https://calmclove.com/",
]
for URL in URLs:
    get_print_keywords(URL)
    get_css_pallete(URL)
