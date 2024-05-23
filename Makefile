install:
	pip3 install -r requirements.txt
	python3 -m spacy download en_core_web_sm
	pip3 install Pillow

serve:
	gunicorn -w 4 -b 0.0.0.0:8000 -k gevent flask_serve:app