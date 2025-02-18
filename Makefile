# 📌 REDCap-EDA Makefile

# 🚀 Run the CLI analysis (Default: Uses sample dataset)
run:
	poetry run redcap-eda analyze

# 🐞 Run CLI in debug mode (Defaults to sample dataset)
debug:
	poetry run redcap-eda --debug analyze

# 🛠️ Run CLI with a user-provided CSV
run-csv:
	poetry run redcap-eda analyze --csv my_data.csv

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
	@tree --prune -I "*~|__pycache__|eda_reports|*.bak"

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

# 📊 Test DatetimeAnalysisMixin interactively
test-datetime:
	poetry run python -i -c "\
	from redcap_eda.analysis.datetime.mixins import DatetimeAnalysisMixin; \
	import pandas as pd; \
	datetime_data = pd.Series(pd.date_range('2022-01-01', periods=5, freq='D')); \
	obj = DatetimeAnalysisMixin(); \
	print(obj.analyze_datetime(datetime_data))"

# 🔬 Test EDA Pipeline interactively
test-eda:
	poetry run python -i -c "\
	from redcap_eda.analysis.eda import ExploratoryDataAnalysis; \
	import pandas as pd; \
	df = pd.DataFrame({'num': [1, 2, 3, 4, 100], 'cat': ['A', 'B', 'A', 'C', 'B'], 'text': ['one', 'two', 'three', None, 'five'], 'date': pd.date_range('2022-01-01', periods=5, freq='D')}); \
	eda = ExploratoryDataAnalysis(df); \
	report = eda.explore(); \
	print(report)"

# 🚀 Test CLI Interactions
test-cli:
	poetry run redcap-eda --help

# 📂 Test CLI with user CSV input
test-cli-csv:
	poetry run redcap-eda analyze --csv my_data.csv

# 📂 List available test cases (Deprecated)
list-cases:
	@echo "⚠️ The concept of 'test cases' is deprecated. Use '--csv' or the default sample."

# 🚀 Debug CLI (Defaults to sample dataset)
debug-cli:
	poetry run redcap-eda --debug analyze

# 🗑️ Clean up generated reports & logs
clean:
	rm -rf eda_reports
	rm -f logs/redcap_eda.log
