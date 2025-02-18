# REDCap-EDA

![CI Status](https://github.com/robertp/REDCap-EDA/actions/workflows/ci.yaml/badge.svg)

## 📌 Overview
REDCap-EDA is a command-line tool for performing **Exploratory Data Analysis (EDA)** on **REDCap datasets**. It automates data inspection, schema enforcement, statistical analysis, and visualization.

## 🚀 Features
- ✅ **Automatic Data Type Enforcement** (casts columns based on a predefined or user-defined schema)
- 📊 **Summary Statistics** (mean, median, std dev, outliers, categorical distributions)
- 📉 **Visualizations** (histograms, box plots, categorical distributions, time trends)
- 🔄 **Multiprocessing for Faster Execution**
- 🔍 **Progress Bars with `tqdm`**
- 📂 **Exports Reports** (JSON, CSV, and saved visualizations)
- 📝 **Interactive Schema Creation** for custom datasets

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/robertp/REDCap-EDA.git
cd REDCap-EDA

# Install dependencies using Poetry
poetry install
```

## 🛠️ Usage

### 🔹 Example Using the Sample Dataset and Interactive Schema Creation
```bash
poetry run redcap-eda analyze --sample
```

### 🔹 Example Using the Sample Dataset with a Predefined Schema
```bash
poetry run redcap-eda analyze --sample --schema schemas/schema_sample_dataset.json
```

### 🔹 Running EDA on a Custom Dataset with Interactive Schema Creation
```bash
poetry run redcap-eda analyze --csv path/to/your_data.csv
```

### 🔹 Running EDA on a Custom Dataset with a Predefined Schema
```bash
poetry run redcap-eda analyze --csv path/to/your_data.csv --schema path/to/schema.json
```

### 🔹 Running in Debug Mode
```bash
poetry run redcap-eda --debug analyze --sample
```

### 🔹 Listing Available Test Cases
```bash
poetry run redcap-eda list-cases
```

### 🔹 Interactive Testing with Makefile
```bash
# Explore a text-based column
make test-text

# Analyze numerical data
make test-numeric

# Inspect categorical variables
make test-categorical

# Run full exploratory analysis interactively
make test-eda
```

## 📂 Project Structure
```bash
.
├── Makefile                # Helper commands
├── README.md               # Project documentation
├── mypy.ini                # Type checking configuration
├── poetry.lock             # Poetry dependency lock file
├── pyproject.toml          # Poetry project configuration
├── schemas                 # Saved schema files
│   └── schema_sample_dataset.json
├── src
│   ├── logs
│   │   └── redcap_eda.log  # Log files
│   └── redcap_eda
│       ├── __init__.py
│       ├── analysis        # EDA analysis modules
│       │   ├── __init__.py
│       │   ├── categorical
│       │   │   ├── __init__.py
│       │   │   └── mixins.py
│       │   ├── datetime
│       │   │   ├── __init__.py
│       │   │   └── mixins.py
│       │   ├── eda.py      # Main EDA module
│       │   ├── numerical
│       │   │   ├── __init__.py
│       │   │   └── mixins.py
│       │   └── text
│       │       ├── __init__.py
│       │       └── mixins.py
│       ├── cast_schema.py  # Schema enforcement
│       ├── cli.py          # Command-line interface
│       ├── load_case_data.py # Dataset loader
│       ├── logger.py       # Logging utilities
└── tests                   # Unit tests
    ├── __init__.py
    └── fixtures
        └── toy_data.csv    # Sample test data
```

## 📝 Contributing
1. **Fork the repository** and create a feature branch.
2. **Run tests** to ensure code integrity:
   ```bash
   poetry run pytest tests/
   ```
3. **Submit a pull request** with a detailed description.

## 📜 License
This project is licensed under the **MIT License**.

## 🤝 Acknowledgments
- [REDCap](https://projectredcap.org/) for enabling structured data collection.
- The **Open Source Community** for inspiration & contributions!
