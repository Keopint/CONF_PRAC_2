@echo off
echo Running application (Stage 2)...
python -m src.main --package requests --repo https://pypi.org --max-depth 3

echo.
echo Running tests...
python -m pytest tests/
pause