# REDCap-EDA

![CI Status](https://github.com/robertp/REDCap-EDA/actions/workflows/ci.yaml/badge.svg)

## 📌 Overview
REDCap-EDA is a command-line tool for performing **Exploratory Data Analysis (EDA)** on **REDCap datasets**. It automates data inspection, schema enforcement, statistical analysis, and visualization.

## 🚀 Features
- ✅ **Automatic Data Type Enforcement** (casts columns based on predefined schema)
- 📊 **Summary Statistics** (mean, median, std dev, outliers)
- 📉 **Visualizations** (histograms, box plots, categorical distributions)
- 🔄 **Multiprocessing for Faster Execution**
- 🔍 **Progress Bars with `tqdm`**
- 📂 **Exports Reports** (JSON, CSV, and saved visualizations)

## 📦 Installation
```bash
# Clone the repository
git clone https://github.com/robertp/REDCap-EDA.git
cd REDCap-EDA

# Install dependencies using Poetry
poetry install
```

## 🛠️ Usage
### 🔹 Running EDA on a REDCap Test Case
```bash
poetry run redcap-eda analyze --case 01
```

### 🔹 Running in Debug Mode
```bash
poetry run redcap-eda --debug analyze --case 01
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
├── Makefile.bak            # Backup of Makefile
├── README.md               # Project documentation
├── mypy.ini                # Type checking configuration
├── poetry.lock             # Poetry dependency lock file
├── pyproject.toml          # Poetry project configuration
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
    └── test_load_case_data.py
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
