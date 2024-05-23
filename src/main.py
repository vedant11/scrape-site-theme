import argparse
from options import CSSKWInterface

parser = argparse.ArgumentParser(description="Process some URLs.")
parser.add_argument(
    "URLs", metavar="URL", type=str, nargs="+", help="an URL to process"
)
args = parser.parse_args()

for URL in args.URLs:
    print(CSSKWInterface.get_css_kw_spacy_ranked(URL))
