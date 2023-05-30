.PHONY: run clean install

install:
	pip install mlconjug3
	pip install spacy
	python3.10 -m spacy download fr_core_news_sm

run:
	@echo "Running the program..."
	python3 src/conjugaisons.py

clean:
	@echo "Cleaning up..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete