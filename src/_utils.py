# Importing necessary modules
import argparse
import base64
import io
import json
import os
import re
import sys
import time
from collections import OrderedDict, namedtuple

import en_core_web_sm
import numpy as np
import requests
import scipy
import spacy
from bs4 import BeautifulSoup
from config import url2colors_headers
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.common.by import By
from spacy.lang.en.stop_words import STOP_WORDS


nlp = spacy.load("en_core_web_sm")


class _Utils:
    class SpacyTextRank4Keyword:
        """Extract keywords from text"""

        def __init__(self):
            self.d = 0.85  # damping coefficient, usually is .85
            self.min_diff = 1e-5  # convergence threshold
            self.steps = 10  # iteration steps
            self.node_weight = None  # save keywords and its weight

        def set_stopwords(self, stopwords):
            """Set stop words"""
            for word in STOP_WORDS.union(set(stopwords)):
                lexeme = nlp.vocab[word]
                lexeme.is_stop = True

        def sentence_segment(self, doc, candidate_pos, lower):
            """Store those words only in cadidate_pos"""
            sentences = []
            for sent in doc.sents:
                selected_words = []
                for token in sent:
                    # Store words only with cadidate POS tag
                    if token.pos_ in candidate_pos and token.is_stop is False:
                        if lower is True:
                            selected_words.append(token.text.lower())
                        else:
                            selected_words.append(token.text)
                sentences.append(selected_words)
            return sentences

        def get_vocab(self, sentences):
            """Get all tokens"""
            vocab = OrderedDict()
            i = 0
            for sentence in sentences:
                for word in sentence:
                    if word not in vocab:
                        vocab[word] = i
                        i += 1
            return vocab

        def get_token_pairs(self, window_size, sentences):
            """Build token_pairs from windows in sentences"""
            token_pairs = list()
            for sentence in sentences:
                for i, word in enumerate(sentence):
                    for j in range(i + 1, i + window_size):
                        if j >= len(sentence):
                            break
                        pair = (word, sentence[j])
                        if pair not in token_pairs:
                            token_pairs.append(pair)
            return token_pairs

        def symmetrize(self, a):
            return a + a.T - np.diag(a.diagonal())

        def get_matrix(self, vocab, token_pairs):
            """Get normalized matrix"""
            # Build matrix
            vocab_size = len(vocab)
            g = np.zeros((vocab_size, vocab_size), dtype="float")
            for word1, word2 in token_pairs:
                i, j = vocab[word1], vocab[word2]
                g[i][j] = 1

            # Get Symmeric matrix
            g = self.symmetrize(g)

            # Normalize matrix by column
            norm = np.sum(g, axis=0)
            g_norm = np.divide(
                g, norm, where=norm != 0
            )  # this is ignore the 0 element in norm

            return g_norm

        def get_keywords(self, number=10):
            """Return an array of top number keywords"""
            node_weight = OrderedDict(
                sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True)
            )
            keywords = []
            for i, (key, value) in enumerate(node_weight.items()):
                if i >= number:
                    break
                keywords.append(key)
            return keywords

        def analyze(
            self,
            text,
            candidate_pos=["NOUN", "PROPN"],
            window_size=4,
            lower=False,
            stopwords=list(),
        ):
            """Main function to analyze text"""

            # Set stop words
            self.set_stopwords(stopwords)

            # Pare text by spaCy
            doc = nlp(text)

            # Filter sentences
            sentences = self.sentence_segment(
                doc, candidate_pos, lower
            )  # list of list of words

            # Build vocabulary
            vocab = self.get_vocab(sentences)

            # Get token_pairs from windows
            token_pairs = self.get_token_pairs(window_size, sentences)

            # Get normalized matrix
            g = self.get_matrix(vocab, token_pairs)

            # Initionlization for weight(pagerank value)
            pr = np.array([1] * len(vocab))

            # Iteration
            previous_pr = 0
            for epoch in range(self.steps):
                pr = (1 - self.d) + self.d * np.dot(g, pr)
                if abs(previous_pr - sum(pr)) < self.min_diff:
                    break
                else:
                    previous_pr = sum(pr)

            # Get weight for each node
            node_weight = dict()
            for word, index in vocab.items():
                node_weight[word] = pr[index]

            self.node_weight = node_weight

    class SSToPalette:
        """use generate method"""

        @staticmethod
        def _get_colors(image, numcolors=10, resize=150):
            # Resize image to speed up processing
            img = image.copy()
            img = img.copy()
            img.thumbnail((resize, resize))

            # Reduce to palette
            paletted = img.convert("P", palette=Image.ADAPTIVE, colors=numcolors)

            # Find dominant colors
            palette = paletted.getpalette()
            color_counts = sorted(paletted.getcolors(), reverse=True)
            colors = list()
            for i in range(numcolors):
                palette_index = color_counts[i][1]
                dominant_color = palette[palette_index * 3 : palette_index * 3 + 3]
                colors.append(tuple(dominant_color))

            return colors

        @staticmethod
        def _save_palette(colors, swatchsize=20, outfile="palette.png"):
            num_colors = len(colors)
            palette = Image.new("RGB", (swatchsize * num_colors, swatchsize))
            draw = ImageDraw.Draw(palette)

            posx = 0
            for color in colors:
                draw.rectangle([posx, 0, posx + swatchsize, swatchsize], fill=color)
                posx = posx + swatchsize

            del draw
            if not os.path.exists(outfile):
                os.makedirs(os.path.dirname(outfile), exist_ok=True)
            palette.save(outfile, "PNG")

        @staticmethod
        def generate(image: Image):
            colors = _Utils.SSToPalette._get_colors(image)
            # _Utils.SSToPalette._save_palette(colors, outfile="./generated/")
            return colors

    def cluster_colors(palette: list):
        # Convert image to an array of RGB values
        ar = np.asarray(palette)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)

        # Perform K-means clustering
        codes, _ = scipy.cluster.vq.kmeans(ar, 4)

        # Assign codes to image pixels
        vecs, _ = scipy.cluster.vq.vq(ar, codes)

        # Count occurrences of each cluster
        counts, _ = scipy.histogram(vecs, len(codes))

        # Find the most frequent cluster (dominant color)
        index_max = scipy.argmax(counts)
        peak = codes[index_max]

        # Convert the dominant color to hexadecimal
        color = "#{:02x}{:02x}{:02x}".format(*map(int, peak))
        print(f"Most frequent color is {peak} ({color})")

    def get_page_source(URL):
        """Uses Selenium to get the page source
        Parsed by BeautifulSoup
        """
        driver = webdriver.Chrome()

        driver.get(URL)
        time.sleep(3)  # experiment with timer to fetch all the data
        page = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page, "html.parser")
        text = soup.get_text(separator=" ")

        meta_tag = soup.find("meta", attrs={"name": "description"})
        description = meta_tag["content"] if meta_tag else ""

        clean_text = re.sub(r"\s+", " ", text + " " + description)
        return clean_text

    def get_url_txt_slnm(URL) -> str:
        """
        url_txt:str = get_url_txt_slnm("https://www.google.com")
        """
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("start-maximized")
        options.experimental_option("useAutomationExtension", False)
        options.experimental_option("excludeSwitches", ["enable-automation"])
        driver = webdriver.Chrome(options=options)
        """
        driver = webdriver.Chrome()
        driver.get(URL)
        time.sleep(5)
        url_txt = driver.find_element(By.XPATH, "/html/body").text
        driver.close()
        return url_txt

    def get_url_txt_bs(URL) -> str:
        """
        url_txt:str = get_url_txt_bs("https://www.google.com")
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        url_txt = soup.get_text()
        return url_txt

    def get_webpage_ss(URL) -> Image:
        """
        pil_ss:Image = get_webpage_ss("https://www.google.com")
        pil_ss.show()
        """
        driver = webdriver.Chrome()
        driver.get(URL)
        time.sleep(5)

        screenshot_base64 = driver.get_screenshot_as_base64()
        screenshot_image = Image.open(io.BytesIO(base64.b64decode(screenshot_base64)))

        driver.close()
        return screenshot_image

    def generate_and_save_html_from_css_palette(URL, *palette) -> None:
        """
        save generated HTML file to ./generated/htmls/<domain>/generated_index.html
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{palette[0]} and {palette[1]} Theme</title>
            <style>
                body {{
                    background-color: {palette[1]};
                    color: white;
                    font-family: Arial, sans-serif;
                }}
                h1 {{
                    color: {palette[0]};
                }}
                p {{
                    color: white;
                }}
            </style>
        </head>
        <body>
            <h1>Welcome to My Website!</h1>
            <p>This is a simple website using {palette[0]} and {palette[1]} colors.</p>
        </body>
        </html>
        """
        domain = re.search("https?://(.*)", URL).group(1)
        dir = f"./generated/htmls/{domain}"
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(f"{dir}/generated_index.html", "w") as f:
            f.write(html)
        return None
