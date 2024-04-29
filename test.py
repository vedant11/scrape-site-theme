from script import (
    get_print_keywords,
    get_css_pallete,
    generate_html_from_css_pallete,
    get_webpage_ss,
)

import subprocess

URLs = [
    "https://calmclove.com/",
]
for URL in URLs:
    get_print_keywords(URL)
    get_css_pallete(URL)
    generate_html_from_css_pallete("red", "green")
    get_webpage_ss(URL)
    subprocess.run(
        [
            "python",
            "experiments/image2colors.py",
            "experiments/screenshot.png",
            "experiments/palette.png",
        ]
    )
    colors = ["#000000"]
    with open("./experiments/colors.txt", "rt") as f:
        colors = f.readlines()
    generate_html_from_css_pallete(*colors)
