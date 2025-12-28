.PHONY: install test format lint clean build publish

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

format:
	black src/ tests/

lint:
	flake8 src/ tests/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

publish: build
	python -m twine upload dist/*

example-mismatch:
	chat-template-detector validate \
		--training-file examples/training_chatml.jsonl \
		--inference-config examples/config_llama2.yaml

example-match:
	chat-template-detector validate \
		--training-file examples/training_llama2.jsonl \
		--inference-config examples/config_llama2.yaml
