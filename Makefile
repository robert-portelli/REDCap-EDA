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
import os; \
from redcap_eda import *; \
from redcap_eda.cast_schema import SchemaHandler; \
import importlib; \
from datetime import datetime; \
from redcap_eda.unified_report import UnifiedReport; \
from redcap_eda.load_case_data import load_data; \
logger.set_log_level(debug_mode=True); \
reload = importlib.reload; \
output_dir = 'tests/eda_test_run'; \
os.makedirs(output_dir, exist_ok=True); \
dataset_source = 'TEST Sample Dataset'; \
unified_report = UnifiedReport(output=output_dir, dataset_name='sample dataset'); \
df = load_data(); \
title_page_content = { \
    'source': dataset_source, \
    'rows': df.shape[0], \
    'columns': df.shape[1], \
    'schema': 'testing', \
    'timestamp': datetime.utcnow().isoformat(), \
}; \
unified_report.load_title_page_content(title_page_content); \
schema_handler = SchemaHandler('schemas/schema_sample_dataset.json'); \
schema_handler.load_schema(); \
df, schema_report = schema_handler.enforce_schema(df); \
unified_report.load_schema_enforcement_page_content(schema_report); \
from redcap_eda.analysis.eda import ExploratoryDataAnalysis; \
eda = ExploratoryDataAnalysis(df, output=output_dir, unified_report=unified_report); \
cat = eda.analyze_column('date_dmy'); \
text = eda.analyze_column('notes'); \
num = eda.analyze_column('zip'); \
print(unified_report.analysis_pages)"


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
