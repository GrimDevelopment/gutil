.PHONY: install run repl clean

install:
	@echo "Installing CLI deps..."
	pip install -r requirements.txt

run:
	@echo "Running sample CLI entry (gutil)"
	python -m gutil -h

repl:
	@echo "Starting Codex REPL"
	python -m gutil codex-repl

clean:
	@echo "Cleaning CLI __pycache__"
	rm -rf __pycache__ codex_cli/__pycache__ app/__pycache__ app/**/__pycache__

