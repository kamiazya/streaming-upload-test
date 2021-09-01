.PHONY: lint format

lint:
	# poetry run mypy app
	poetry run flake8 --show-source app
	poetry run poetry run black app --check
	poetry run isort --force-single-line-imports --check app


format:
	poetry run autopep8 -ivr app
	poetry run black app
	poetry run isort --force-single-line-imports app
