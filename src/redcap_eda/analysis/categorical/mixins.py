"""
📌 CategoricalAnalysisMixin: Analyzes categorical columns.

🔹 **Purpose**:
    - Computes **category counts** and **proportions**.
    - Identifies **most/least frequent categories**.
    - Generates **bar plots** for category distribution.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.categorical.mixins import CategoricalAnalysisMixin
    class MyClass(CategoricalAnalysisMixin):
        pass
    obj = MyClass()
    obj.categorize(df["category_column"])
    ```
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class CategoricalAnalysisMixin:
    """Mixin for categorical column analysis."""

    __slots__ = ()

    @staticmethod
    def categorize(series: pd.Series) -> AnalysisResult:
        """Analyzes categorical columns.

        Args:
            series (pd.Series): The categorical series to analyze.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
            #AnalysisResult = namedtuple("AnalysisResult", ["summary", "plots"])
        """
        if series.empty:
            logger.warning(f"⚠️ Skipping empty categorical column: {series.name}")
            return AnalysisResult(
                summary={"error": "Column is empty"},
                plots=[],
            )

        category_counts = series.value_counts()

        summary = {
            "unique_values": series.nunique(),
            "missing_values": series.isnull().sum(),
            "mode": category_counts.idxmax() if not category_counts.empty else None,
            "most_frequent": category_counts.idxmax()
            if not category_counts.empty
            else None,
            "least_frequent": category_counts.idxmin()
            if not category_counts.empty
            else None,
            "category_counts": category_counts.to_dict(),
            "category_proportions": (category_counts / len(series)).to_dict(),
        }

        plots = [
            CategoricalAnalysisMixin.plot_category_distribution(series),
        ]

        return AnalysisResult(summary, plots)

    @staticmethod
    def plot_category_distribution(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Creates a bar plot for categorical data.

        Args:
            series (pd.Series): The categorical series to plot.

        Returns:
            tuple[plt.Figure, str]: The figure object and filename.
        """
        if series.empty:
            logger.warning(
                f"⚠️ No data available for category distribution: {series.name}",
            )
            return None, ""

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.countplot(y=series, order=series.value_counts().index, ax=ax)
        ax.set_title(f"Category Distribution of {series.name}")

        filename = f"{series.name}_category_distribution.png"
        return fig, filename
