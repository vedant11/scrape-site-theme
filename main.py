import argparse
import subprocess

from script import (
    generate_html_from_css_palette,
    get_css_palette,
    get_keywords_bs,
    get_print_keywords,
    get_webpage_ss,
)

parser = argparse.ArgumentParser(description="Process some URLs.")
parser.add_argument(
    "URLs", metavar="URL", type=str, nargs="+", help="an URL to process"
)
args = parser.parse_args()

for URL in args.URLs:
    get_css_palette(URL)
    get_keywords_bs(URL)
    # get_webpage_ss(URL)
    # subprocess.run(
    #     [
    #         "python3",
    #         "experiments/image2colors.py",
    #         "experiments/screenshot.png",
    #         "experiments/palette.png",
    #     ]
    # )
    # colors = []
    # with open("./experiments/colors.txt", "rt") as f:
    #     colors = f.readlines()
    # generate_html_from_css_palette(URL, *colors)
