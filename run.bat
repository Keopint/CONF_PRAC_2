@echo off
echo Running application...
python src/main.py --package requests --repo https://pypi.org --max-depth 3 --test-mode --ascii-tree

echo.
echo Running tests...
python -m pytest tests/
pause