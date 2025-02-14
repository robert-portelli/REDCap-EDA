run:
	poetry run redcap-eda analyze --case 01
test:
	poetry run pytest tests/
tree:
	@tree --prune -I "*~|__pycache__"
