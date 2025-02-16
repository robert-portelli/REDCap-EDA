run:
	poetry run redcap-eda analyze --case 01

debug:
	poetry run redcap-eda --debug analyze --case 01

it:
	poetry run python -i -c "\
	from redcap_eda import *; \
	import importlib; \
	logger.set_log_level(debug_mode=True); \
	reload = importlib.reload; \
	df = load_case_data.load_data(); \
	df, report = cast_schema.enforce_schema(df)"

test:
	poetry run pytest tests/

tree:
	@tree --prune -I "*~|__pycache__"
