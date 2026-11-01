@echo off
echo Running application (Stage 3) - Test Mode...
python -m src.main --package A --repo test_repo.txt --max-depth 3 --test-mode

echo.
echo Running application (Stage 3) - Real Mode...
python -m src.main --package requests --repo https://pypi.org --max-depth 2

echo.
echo Running tests...
python -m pytest tests/
pause