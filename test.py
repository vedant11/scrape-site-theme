from script import get_print_keywords, get_css_pallete, generate_html_from_css_pallete

URLs = [
    "https://calmclove.com/",
]
for URL in URLs:
    get_print_keywords(URL)
    get_css_pallete(URL)
    generate_html_from_css_pallete("red", "green")
