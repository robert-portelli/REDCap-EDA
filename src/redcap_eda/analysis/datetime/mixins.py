"""
📌 DatetimeAnalysisMixin: Analyzes datetime columns.

🔹 **Purpose**:
    - Computes time-based statistics.
    - Extracts meaningful datetime features (year, month, weekday, hour).
    - Generates visualizations for time-based trends.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.datetime.mixins import DatetimeAnalysisMixin
    class MyClass(DatetimeAnalysisMixin):
        pass
    obj = MyClass()
    obj.analyze_datetime(df["timestamp_column"])
    ```
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class DatetimeAnalysisMixin:
    """Mixin for datetime analysis."""

    __slots__ = ()

    @staticmethod
    def analyze_datetime(series: pd.Series) -> AnalysisResult:
        """Analyzes datetime columns & generates time-based visualizations.

        Args:
            series (pd.Series): The datetime series to analyze.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
        """
        logger.debug(f"🕒 Analyzing datetime column: {series.name}")

        if series.empty:
            logger.warning(f"⚠️ Skipping empty datetime column: {series.name}")
            return AnalysisResult(
                summary={"error": "Column is empty"},
                plots=[],
            )

        if not pd.api.types.is_datetime64_any_dtype(series):
            logger.warning(f"⚠️ Column {series.name} is not a datetime type.")
            return AnalysisResult(
                summary={"error": "Not a valid datetime column"},
                plots=[],
            )

        # Compute summary statistics
        summary = {
            "earliest": series.min(),
            "latest": series.max(),
            "time_span": str(series.max() - series.min()),
            "missing_values": series.isnull().sum(),
            "year_counts": series.dt.year.value_counts().to_dict(),
            "month_counts": series.dt.month.value_counts().to_dict(),
            "weekday_counts": series.dt.day_name().value_counts().to_dict(),
            "hour_counts": series.dt.hour.value_counts().to_dict(),
        }

        # Generate plots
        plots = [
            DatetimeAnalysisMixin.plot_datetime_distribution(series),
            DatetimeAnalysisMixin.plot_time_trend(series),
        ]

        return AnalysisResult(summary, plots)

    @staticmethod
    def plot_datetime_distribution(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Plots a histogram of datetime values.

        Args:
            series (pd.Series): The datetime series to plot.

        Returns:
            tuple[plt.Figure, str]: The figure object and filename.
        """
        if series.empty:
            logger.warning(
                f"⚠️ No data available for datetime distribution: {series.name}",
            )
            return None, ""
        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.histplot(series, bins=30, kde=True, ax=ax, color="blue")
            ax.set_title(f"Datetime Distribution of {series.name}")
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Frequency")

            filename = f"{series.name}_datetime_distribution.png"
            return fig, filename

        except Exception as e:
            logger.error(
                f"❌ Error generating datetime distribution for {series.name}: {e}",
            )
            return None, ""

    @staticmethod
    def plot_time_trend(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Plots a line chart showing time-based trends.

        Args:
            series (pd.Series): The datetime series to plot.

        Returns:
            tuple[plt.Figure, str]: The figure object and filename.
        """
        if series.empty:
            logger.warning(f"⚠️ No data available for time trend: {series.name}")
            return None, ""
        try:
            df = pd.DataFrame({series.name: series})
            df = df.set_index(series.name)
            df["count"] = 1
            df = df.resample("D").sum()
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df.index, df["count"], marker="o", linestyle="-", color="blue")
            ax.set_title(f"Time Trend of {series.name}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Count of Records")
            ax.grid()

            filename = f"{series.name}_time_trend.png"
            return fig, filename

        except Exception as e:
            logger.error(f"❌ Error generating time trend plot for {series.name}: {e}")
            return None, ""
