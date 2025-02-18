"""
📌 NumericalAnalysisMixin: Analyzes numerical columns.

🔹 **Purpose**:
    - Computes summary statistics (mean, median, std, min, max, outliers).
    - Generates **histograms** and **boxplots** for visualization.
    - Supports **log scale** and **outlier visibility toggling**.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.numerical.mixins import NumericalAnalysisMixin
    class MyClass(NumericalAnalysisMixin):
        pass
    obj = MyClass()
    obj.summarize(df["age"])
    ```
"""

from collections import namedtuple
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from redcap_eda.logger import logger


class NumericalAnalysisMixin:
    """Mixin for numerical analysis."""

    __slots__ = ()

    AnalysisResult = namedtuple("AnalysisResult", ["summary", "plots"])

    @staticmethod
    def summarize(series: pd.Series) -> AnalysisResult:
        """Analyze numerical columns (int/float) & generate plots.

        Args:
            series (pd.Series): The numerical series to analyze.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
        """
        if series.empty:
            logger.warning(f"⚠️ Skipping empty numerical column: {series.name}")
            return NumericalAnalysisMixin.AnalysisResult(
                summary={"error": "Column is empty"},
                plots=[],
            )

        # Compute summary statistics
        summary = {
            "mean": series.mean(),
            "median": series.median(),
            "std_dev": series.std(),
            "min": series.min(),
            "max": series.max(),
            "outliers": NumericalAnalysisMixin.detect_outliers(series),
        }

        # Generate plots (store file paths)
        plots = [
            NumericalAnalysisMixin.plot_distribution(series),
            NumericalAnalysisMixin.plot_boxplot(series),
        ]

        return NumericalAnalysisMixin.AnalysisResult(summary, plots)

    @staticmethod
    def detect_outliers(series):
        """Detect outliers using the IQR method."""
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return series[(series < lower_bound) | (series > upper_bound)].tolist()

    @staticmethod
    def plot_distribution(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Plots a histogram & KDE for numerical data and saves the file.

        Args:
            series (pd.Series): The numerical series to plot.

        Returns:
            str: The file path of the saved plot.
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for histogram: {series.name}")
            return None, ""

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(series, bins=20, kde=True, ax=ax)
        ax.set_title(f"Distribution of {series.name}")

        filename = f"{series.name}_distribution.png"
        return fig, filename

    @staticmethod
    def plot_boxplot(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Plots a boxplot for numerical data and saves the file.

        Args:
            series (pd.Series): The numerical series to plot.

        Returns:
            str: The file path of the saved plot.
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for boxplot: {series.name}")
            return None, ""

        fig, ax = plt.subplots(figsize=(4, 6))
        sns.boxplot(y=series, ax=ax)
        ax.set_title(f"Boxplot of {series.name}")

        filename = f"{series.name}_boxplot.png"
        return fig, filename
