.PHONY: dev migrate makemigrations shell test

# Django development server
dev:
	uv run ragui examples/main.py

# Database migrations
migrate:
	uv run src/ragui/manage.py makemigrations
	uv run src/ragui/manage.py migrate

# Django shell
shell:
	uv run src/ragui/manage.py shell

# Run tests
test:
	uv run pre-commit run --all-files

# Help
help:
	@echo "Available commands:"
	@echo "  dev        - Run Django development server"
	@echo "  migrate    - Run Django database migrations"
	@echo "  shell      - Run Django shell"
	@echo "  test       - Run tests"
	@echo "  help       - Show this help message"
