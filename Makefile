.PHONY: setup lint_api lint format test create_sample_json

setup:
	poetry config virtualenvs.create false
	cd api && poetry install
	cd $(CURDIR)
	cd spa && yarn install

create_sample_json:
	mkdir -p dist
	python ./api/scripts/sample_json.py ./dist/person_100.json 100
	python ./api/scripts/sample_json.py ./dist/person_1000.json 1000
	python ./api/scripts/sample_json.py ./dist/person_10000.json 10000
	python ./api/scripts/sample_json.py ./dist/person_100000.json 100000
