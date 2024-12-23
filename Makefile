.PHONY: install serve

install:
	pip3 install -r requirements.txt
	python3 -m spacy download en_core_web_sm
	pip3 install Pillow

install_chrome:
		curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | sudo gpg --dearmor | sudo tee /usr/share/keyrings/google-chrome.gpg >> /dev/null
		echo deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main | sudo tee /etc/apt/sources.list.d/google-chrome.list
		sudo apt update
		sudo apt install google-chrome-stable -y

serve:
	gunicorn -w 4 -b 0.0.0.0:8000 -k gevent flask_serve:app