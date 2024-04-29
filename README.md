# scrapt-site-theme

extracts keywords and CSS for website theming

## Usage

`generate an HTML with color themes extracted from a URL`

```py
from script import (
    generate_html_from_css_pallete,
    get_webpage_ss,
)

import subprocess

URLs = [
    "https://calmclove.com/",
]
for URL in URLs:
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

```

## Tech

### Keywords

can use either of:

spaCy
YAKE
Rake-Nltk
Gensim

### CSS

#### can use

> $ pip install colorthief
