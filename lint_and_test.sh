#!/bin/bash

echo "------- run black -------"
poetry run black --check ./

echo "------- run isort -------"
poetry run isort --check ./

echo "------- run autoflake -------"
poetry run autoflake -r --check ./

echo "------- run mypy -------"
poetry run mypy ./

echo "------- run pytest -------"
poetry run python -m pytest .
