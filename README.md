# scrapt-site-theme

extracts keywords and CSS for website theming

## Installation

```sh
make install
```

## Usage

generate an HTML with color themes extracted from a URL

```sh
python3 main.py https://example.org
```

or

1. start a server to view to generate the HTML

    ```sh
    python3 serve.py
    ```

2. url in the address bar to generate

    > http://localhost:8000/https://example.org

3. load using
    > http://localhost:8000/~load~example.org

## Tech

### Todo

-   Cluster similar colors
-   Design a template that can include variety of colors from the palette

### Keywords

can use either of:

spaCy
YAKE
Rake-Nltk
Gensim

### CSS

#### can use

> $ pip install colorthief
