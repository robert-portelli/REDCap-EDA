"""
📌 eda.py: Orchestrates Exploratory Data Analysis (EDA) for REDCap datasets.

🔹 **Purpose**:
    - Distributes analysis across multiple column types.
    - Uses **parallel execution** with `multiprocessing` for efficiency.
    - Tracks progress with `tqdm` for user feedback.
    - **Saves visualizations dynamically based on column data type**.

🔹 **Why Use Parallel Processing?**
    - REDCap datasets often have **hundreds of columns**.
    - **Single-threaded execution is slow**, especially for large datasets.
    - `multiprocessing.Pool` allows **CPU-bound tasks to run in parallel**.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.eda import ExploratoryDataAnalysis
    df, report = ExploratoryDataAnalysis(df).explore()
    ```
"""

import os
import json
import numpy as np
import pandas as pd
import multiprocessing as mp
from tqdm import tqdm
import matplotlib.pyplot as plt
from redcap_eda.logger import logger
from redcap_eda.analysis.numerical.mixins import NumericalAnalysisMixin
from redcap_eda.analysis.categorical.mixins import CategoricalAnalysisMixin
from redcap_eda.analysis.text.mixins import TextAnalysisMixin
from redcap_eda.analysis.lib import AnalysisResult


class ExploratoryDataAnalysis(
    NumericalAnalysisMixin,
    CategoricalAnalysisMixin,
    TextAnalysisMixin,
):
    """Performs Exploratory Data Analysis (EDA) on a DataFrame."""

    def __init__(self, df: pd.DataFrame, output_dir="eda_reports"):
        self.df = df
        self.output_dir = os.path.join(
            output_dir,
            f"eda_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_column(self, col: str) -> dict[str, dict | str]:
        """Analyze a single column and save visualizations.

        Args:
            col (str): Column name.

        Returns:
            dict[str, dict | str]: Column analysis result.
        """

        dtype = str(self.df[col].dtype)

        try:
            products: AnalysisResult  # declare to soothe mypy no-redef
            match dtype:
                case "int64" | "float64":
                    products = super().summarize(self.df[col])

                case "category":
                    products = super().categorize(self.df[col])

                case _ if "string" in dtype:  # handles string[python]
                    products = super().analyze_text(self.df[col])

                case _:
                    return {col: {"message": f"Skipped analysis for {dtype} columns"}}

            for fig, filename in products.plots:
                if fig:
                    self.save_plot(fig, filename)

            return {col: products.summary}

        except Exception as e:
            logger.error(f"❌ Error analyzing column {col}: {e}")
            return {col: {"error": str(e)}}  # Wrap errors in a dict

    def explore(self) -> dict[str, dict]:
        """Runs parallel EDA with optimized multiprocessing."""
        logger.info("🚀 Starting Exploratory Data Analysis...")

        column_list = list(self.df.columns)
        num_workers = min(mp.cpu_count(), len(column_list))
        chunksize = max(1, len(column_list) // (num_workers * 2))

        with mp.Pool(num_workers) as pool:
            results = list(
                tqdm(
                    pool.imap(self.analyze_column, column_list, chunksize),
                    total=len(column_list),
                    desc="🔍 Analyzing Columns",
                    unit="col",
                ),
            )

        # Collect only the summary statistics for final report
        report = {col: result[col] for result in results for col in result}

        self.save_report(report)

        logger.info("✅ EDA Complete! Report saved.")
        return report

    def save_plot(self, fig: plt.Figure, filename: str) -> None:
        """Saves a matplotlib figure.

        Args:
            fig (plt.Figure): The Matplotlib figure object.
            filename (str): The the filename to save the plot as.

        Returns:
            None
        """
        try:
            plot_path = os.path.join(self.output_dir, filename)
            fig.savefig(plot_path)
            plt.close(fig)  # Free memory
            logger.info(f"✅ Plot saved as {plot_path}")
        except Exception as e:
            logger.error(f"❌ Error saving plot: {e}")

    def save_report(self, report: dict[str, dict], display: bool = False) -> None:
        """Saves the analysis report as JSON and optionally displays it.

        🔹 **Purpose**:
            - Converts the column-wise analysis results into a structured JSON format.
            - Handles potential issues with NumPy and Pandas data types during serialization.
            - Optionally displays the report in a readable format.

        🔹 **Args**:
            - `report` (dict[str, dict]): Dictionary where each key is a column name and
              the value is a dictionary containing statistical summaries and analysis results.
            - `display` (bool, optional): If `True`, calls `display_report` after saving. Defaults to `False`.

        🔹 **Handling JSON Serialization**:
            - Converts NumPy `int64`, `float64`, and `ndarray` values to standard Python types (`int`, `float`, `list`).
            - Uses Pandas `DataFrame` to normalize dictionary values before saving.

        Example(s):
            # analyze all the columns in a df
            >>> eda = ExploratoryDataAnalysis(df)
            >>> all_columns = {col: eda.analyze_column(col) for col in df.columns}
            >>> eda.save_report(all_columns) # just save the report
            >>> eda.save_report(all_columns, display=True) # # Just save the report

        """
        json_path = os.path.join(self.output_dir, "eda_report.json")

        try:
            # Convert to DataFrame to handle numpy values to json
            # df_report = pd.DataFrame.from_dict(report, orient="index")

            # Save as JSON (pretty-formatted for readability)
            # df_report.to_json(json_path, orient="index", indent=4)

            # Convert and serialize while handling NumPy types
            json_data = json.dumps(
                report,
                indent=4,
                default=lambda x: x.item() if isinstance(x, np.generic) else str(x),
            )

            # Write to file
            with open(json_path, "w") as f:
                f.write(json_data)

            logger.info(f"📂 Saved EDA report to {json_path}")

            if display:
                self.display_report(json_path)

        except Exception as e:
            logger.error(f"❌ Error saving report: {e}")

    @staticmethod
    def display_report(json_path: str) -> None:
        """Loads and displays the EDA report from a JSON file in a human-readable format.

        🔹 **Purpose**:
            - Reads the saved analysis report from a JSON file.
            - Formats and logs the report for easy inspection.
            - Handles errors if the file is missing or malformed.

        🔹 **Args**:
            - `json_path` (str): The path to the saved JSON report.

        🔹 **Example Usage**:
        ```python
        ExploratoryDataAnalysis.display_report("eda_reports/eda_20240216_120000/eda_report.json")
        ```
        """
        if not os.path.exists(json_path):
            logger.error(f"❌ Report file not found: {json_path}")
            return

        try:
            with open(json_path) as f:
                report = json.load(f)

            logger.info(f"📂 Loaded EDA report from {json_path}\n")

            # Format and print the report in a human-readable format
            for col, stats in report.items():
                print(f"📌 Column: {col}")
                if isinstance(stats, dict):
                    for key, value in stats.items():
                        print(f"   - {key}: {value}")
                else:
                    print(f"   - {stats}")  # Handles error messages or skipped analysis
                print("-" * 40)

        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON: {e}")
        except Exception as e:
            logger.error(f"❌ Error loading report: {e}")
