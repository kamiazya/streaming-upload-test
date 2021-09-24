.PHONY: lint format test

lint:
	poetry run mypy src
	poetry run flake8 --show-source src
	poetry run poetry run black src --check
	poetry run isort --force-single-line-imports --check src


format:
	poetry run autopep8 -ivr src
	poetry run black src
	poetry run isort --force-single-line-imports src

test:
	PYTHONPATH=./src poetry run pytest
