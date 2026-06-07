.PHONY: help setup install run dev run-verbose run-nologo clean test check-env freeze activate venv-info

help:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  NewsGenie - Development Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  SETUP & INSTALLATION"
	@echo "    make setup          Create venv and install dependencies"
	@echo "    make install        Install dependencies in existing venv"
	@echo "    make activate       Print venv activation command"
	@echo "    make freeze         Update requirements.txt with current versions"
	@echo ""
	@echo "  RUNNING THE APP"
	@echo "    make run            Run Streamlit app (production mode)"
	@echo "    make dev            Run Streamlit app (dev mode, debug logging)"
	@echo "    make run-verbose    Run Streamlit app with verbose logging"
	@echo "    make run-nologo     Run Streamlit app without Streamlit branding"
	@echo ""
	@echo "  DEVELOPMENT"
	@echo "    make check-env      Verify API keys and environment setup"
	@echo "    make venv-info      Show virtual environment info"
	@echo "    make test           Run tests (not yet implemented)"
	@echo ""
	@echo "  CLEANUP"
	@echo "    make clean          Remove venv, cache, and compiled files"
	@echo "    make clean-cache    Remove only Python cache files"
	@echo "    make clean-venv     Remove only virtual environment"
	@echo ""

# Setup & Installation
setup:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip setuptools wheel
	. venv/bin/activate && pip install -r requirements.txt
	cp .env.example .env
	cp ai/.env.example ai/.env 2>/dev/null || cp .env.example ai/.env
	@echo ""
	@echo "✓ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Activate venv:  source venv/bin/activate"
	@echo "  2. Add API keys to .env and ai/.env"
	@echo "  3. Run app:        make dev"
	@echo ""

install:
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

freeze:
	pip freeze > requirements.txt
	@echo "✓ requirements.txt updated"

activate:
	@echo "Run this to activate the virtual environment:"
	@echo "  source venv/bin/activate"

venv-info:
	@echo "Python version:"
	@python --version
	@echo ""
	@echo "Virtual environment:"
	@if [ -d "venv" ]; then echo "✓ Found at ./venv"; else echo "✗ Not found"; fi
	@echo ""
	@echo "Installed packages:"
	@pip list | head -15

check-env:
	@echo "Checking environment setup..."
	@if [ -f ".env" ]; then echo "✓ .env file exists"; else echo "✗ Missing .env"; fi
	@if [ -f "ai/.env" ]; then echo "✓ ai/.env file exists"; else echo "✗ Missing ai/.env"; fi
	@if grep -q "ANTHROPIC_API_KEY" .env 2>/dev/null; then \
		if grep -q "your_anthropic_api_key_here" .env; then \
			echo "⚠ ANTHROPIC_API_KEY not configured"; \
		else \
			echo "✓ ANTHROPIC_API_KEY configured"; \
		fi; \
	fi
	@if grep -q "NEWS_API_KEY" .env 2>/dev/null; then \
		if grep -q "your_newsapi_key_here" .env; then \
			echo "⚠ NEWS_API_KEY not configured"; \
		else \
			echo "✓ NEWS_API_KEY configured"; \
		fi; \
	fi

# Running the App
run:
	streamlit run ui/app.py

dev:
	streamlit run ui/app.py --logger.level=debug

run-verbose:
	streamlit run ui/app.py --logger.level=debug --client.logger.level=debug

run-nologo:
	streamlit run ui/app.py --client.showErrorDetails=true --client.toolbarMode=viewer

# Cleanup
clean:
	@echo "Cleaning up..."
	rm -rf venv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .streamlit 2>/dev/null || true
	rm -rf .pytest_cache 2>/dev/null || true
	@echo "✓ Clean complete"

clean-cache:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .pytest_cache 2>/dev/null || true
	@echo "✓ Cache cleaned"

clean-venv:
	rm -rf venv
	@echo "✓ Virtual environment removed"

# Testing
test:
	@echo "Tests not yet implemented"
	@echo "Run: pytest tests/"
