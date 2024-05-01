install:
	pip3 install -r requirements.txt
	python3 -m spacy download en_core_web_sm
	pip3 install Pillow