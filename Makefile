# 📌 REDCap-EDA Makefile

# 🚀 Run the CLI analysis
run:
	poetry run redcap-eda analyze --case 01

# 🐞 Run CLI in debug mode
debug:
	poetry run redcap-eda --debug analyze --case 01

# 🛠️ Enter interactive Python session (CLI + Logging)
it:
	poetry run python -i -c "\
	from redcap_eda import *; \
	import importlib; \
	logger.set_log_level(debug_mode=True); \
	reload = importlib.reload; \
	df = load_case_data.load_data(); \
	df, report = cast_schema.enforce_schema(df)"

# 📝 Run Pytest
test:
	poetry run pytest tests/

# 🌳 Show project structure
tree:
	@tree --prune -I "*~|__pycache__"

# 📊 Test TextAnalysisMixin interactively
test-text:
	poetry run python -i -c "\
	from redcap_eda.analysis.text.mixins import TextAnalysisMixin; \
	import pandas as pd; \
	text_data = pd.Series(['Short', 'A much longer sentence.', 'Another entry.', None]); \
	obj = TextAnalysisMixin(); \
	print(obj.analyze_text(text_data))"

# 📊 Test NumericalAnalysisMixin interactively
test-numeric:
	poetry run python -i -c "\
	from redcap_eda.analysis.numerical.mixins import NumericalAnalysisMixin; \
	import pandas as pd; \
	numeric_data = pd.Series([1, 5, 8, 12, 20, 100, 200, 5, None]); \
	obj = NumericalAnalysisMixin(); \
	print(obj.summarize(numeric_data))"

# 📊 Test CategoricalAnalysisMixin interactively
test-categorical:
	poetry run python -i -c "\
	from redcap_eda.analysis.categorical.mixins import CategoricalAnalysisMixin; \
	import pandas as pd; \
	category_data = pd.Series(['A', 'B', 'A', 'C', 'B', 'A', None]); \
	obj = CategoricalAnalysisMixin(); \
	print(obj.categorize(category_data))"

# 🔬 Test EDA Pipeline interactively
test-eda:
	poetry run python -i -c "\
	from redcap_eda.analysis.eda import ExploratoryDataAnalysis; \
	import pandas as pd; \
	df = pd.DataFrame({'num': [1, 2, 3, 4, 100], 'cat': ['A', 'B', 'A', 'C', 'B'], 'text': ['one', 'two', 'three', None, 'five']}); \
	eda = ExploratoryDataAnalysis(df); \
	report = eda.explore(); \
	print(report)"

# 🚀 Test CLI Interactions
test-cli:
	poetry run redcap-eda --help

# 📂 List available test cases
list-cases:
	poetry run redcap-eda list-cases

# 🚀 Debug CLI
debug-cli:
	poetry run redcap-eda --debug analyze --case 01

# 🗑️ Clean up generated reports & logs
clean:
	rm -rf eda_reports
	rm -f logs/redcap_eda.log
