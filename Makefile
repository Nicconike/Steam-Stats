# Makefile for Steam Stats project

.PHONY: help install run clean

help: ## Display this help section
	@echo "The following commands can be used:"
	@echo ""
	@echo "make install  - Install dependencies"
	@echo "make run      - Run the application"
	@echo "make clean    - Clean up the project"
	@echo ""

install: ## Install dependencies
	@pip install -r requirements.txt

run: ## Run the application
	@python api/main.py

clean: ## Clean up the project
	@rm -rf __pycache__
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
