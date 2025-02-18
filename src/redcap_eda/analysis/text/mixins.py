"""
📌 TextAnalysisMixin: Analyzes text-based columns.

🔹 **Purpose**:
    - Analyzes text length distribution.
    - Detects missing values & unique text entries.
    - Identifies the most frequently occurring words.
    - Generates a word cloud visualization for top words.

🔹 **Example Usage**:
    ```python
    from redcap_eda.analysis.text.mixins import TextAnalysisMixin
    class MyClass(TextAnalysisMixin):
        pass
    obj = MyClass()
    obj.analyze_text(df["text_column"])
    ```
"""

from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from redcap_eda.logger import logger
from redcap_eda.analysis.lib import AnalysisResult


class TextAnalysisMixin:
    """Mixin for analyzing text-based data."""

    __slots__ = ()

    @staticmethod
    def analyze_text(series: pd.Series) -> AnalysisResult:
        """Analyzes text-based data & generates visualizations.

        Args:
            series (pd.Series): The text series to analyze.

        Returns:
            AnalysisResult: Named tuple containing summary statistics and plots.
            #AnalysisResult = namedtuple("AnalysisResult", ["summary", "plots"])
        """
        if series.empty:
            logger.warning(f"⚠️ Skipping empty text column: {series.name}")
            return AnalysisResult(
                summary={"error": "Column is empty"},
                plots=[],
            )

        text_lengths = series.dropna().str.len()
        word_counts = Counter(" ".join(series.dropna()).split())

        summary = {
            "unique_values": series.nunique(),
            "missing_values": series.isnull().sum(),
            "average_length": text_lengths.mean(),
            "min_length": text_lengths.min(),
            "max_length": text_lengths.max(),
            "top_words": dict(word_counts.most_common(10)),
        }

        plots = [
            TextAnalysisMixin.plot_text_length_distribution(text_lengths),
            TextAnalysisMixin.generate_wordcloud(series),
        ]

        return AnalysisResult(summary, plots)

    @staticmethod
    def plot_text_length_distribution(
        series: pd.Series,
    ) -> tuple[plt.Figure | None, str]:
        """Plots a histogram for text length distribution.

        Args:
            series (pd.Series): Series containing text lengths.

        Returns:
            tuple[plt.Figure, str]: The figure object and filename.
        """
        if series.empty:
            logger.warning("⚠️ No valid text lengths available for plotting.")
            return None, ""

        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(series, bins=20, kde=True, ax=ax, color="purple")
        ax.set_title(f"Text Length Distribution (n={len(series)})")
        ax.set_xlabel("Character Count")
        ax.set_ylabel("Frequency")

        filename = f"{series.name}_text_length_distribution.png"
        return fig, filename

    @staticmethod
    def generate_wordcloud(series: pd.Series) -> tuple[plt.Figure | None, str]:
        """Generates a word cloud visualization from text data.

        Args:
            series (pd.Series): The text series to analyze.

        Returns:
            tuple[plt.Figure, str]: The figure object and filename.
        """
        text = " ".join(series.dropna().astype(str))
        if not text.strip():
            logger.warning(f"⚠️ Skipping word cloud for {series.name}: No words found.")
            return None, ""

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            text,
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Word Cloud for {series.name}")

        filename = f"{series.name}_wordcloud.png"
        return fig, filename
