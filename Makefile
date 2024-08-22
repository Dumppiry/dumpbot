dev:
	PYENV=DEV python3 src/main.py

prod:
	PYENV=PROD python3 src/main.py

freeze:
	pip freeze > requirements.txt