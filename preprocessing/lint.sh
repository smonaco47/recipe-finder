poetry run isort src
poetry run flake8 src
poetry run black src
poetry run mypy src