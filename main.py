import argparse
import subprocess

from script import (
    generate_html_from_css_pallete,
    get_webpage_ss,
)

from keywords import (
    scrape_website,
    TextRank4Keyword
)

parser = argparse.ArgumentParser(description="Process some URLs.")
parser.add_argument(
    "URLs", metavar="URL", type=str, nargs="+", help="an URL to process"
)
args = parser.parse_args()

for URL in args.URLs:
    get_webpage_ss(URL)
    subprocess.run(
        [
            "python3",
            "experiments/image2colors.py",
            "experiments/screenshot.png",
            "experiments/palette.png",
        ]
    )
    colors = []
    with open("./experiments/colors.txt", "rt") as f:
        colors = f.readlines()
    generate_html_from_css_pallete(URL, *colors)
    
    clean_text = scrape_website(URL)
    tr4w = TextRank4Keyword()
    tr4w.analyze(clean_text, candidate_pos = ['NOUN', 'PROPN'], window_size=4, lower=False)
    keywords = tr4w.get_keywords(10)
    print(keywords)
