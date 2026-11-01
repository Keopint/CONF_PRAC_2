@echo off
echo Running application (Stage 4) - Install Order (Test Mode)...
python -m src.main --package A --repo test_repo.txt --max-depth 3 --test-mode --install-order

echo.
echo Running application (Stage 4) - Install Order (Real Mode)...
python -m src.main --package requests --repo https://pypi.org --max-depth 2 --install-order

echo.
echo Running tests...
python -m pytest tests/
pause