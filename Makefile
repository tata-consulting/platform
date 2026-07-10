.PHONY: build serve

build:
	@echo "Generating site..."
	python3 scripts/generate-site.py

serve: build
	@echo "Serving site at http://localhost:8000"
	python3 -m http.server --directory site 8000

