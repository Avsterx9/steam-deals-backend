.PHONY: build

help:
	@echo "AVAILABLE COMMANDS WITH MAKE:"
	@echo "     clean - remove 'venv/' directory"
	@echo "     build - build entire project in 'venv/'"
	@echo "     build-clean - remove 'venv/' directory and build entire project again in 'venv/'"
	@echo "     black-check - check formatting with Black"
	@echo "     black-write - fix formatting with Black"
	@echo "     lint - lint code with pylint"
	@echo "     test - run all tests"
	@echo "     run - run application"

build-clean: clean build

clean:
	rm -r venv/

build:
	./scripts/secrets-create.sh
	python3 -m venv venv/
	. venv/bin/activate
	pip install -U pip setuptools wheel
	pip install -e .[dev]

black-check:
	black . --diff --color

black-write:
	black .

lint:
	pylint steam_deals/ tests/

test:
	pytest tests/

run:
	steam-deals
