import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level
from redcap.eda.cast_schema import enforce_schema
from redcap_eda.analysis import (
    check_data_quality,
    compute_summary_statistics,
    compute_correlations,
)
from redcap_eda.visualization import (
    plot_histogram,
    plot_boxplot,
    plot_correlation_matrix,
)


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose debug logging")
def cli(debug):
    """REDCap-EDA: Perform Exploratory Data Analysis on REDCap datasets."""
    set_log_level(debug)


@click.command()
@click.option(
    "--case",
    required=True,
    help="Specify the REDCap test case (e.g., 01, 07, 20)",
)
def analyze(case):
    """Perform EDA on the specified REDCap test dataset."""

    logger.info(f"🔍 Loading Case {case}...")

    try:
        # Load datasets (handling missing data)
        if not (df := load_data()):
            logger.error(f"❌ Case {case} lacks records for analysis.")
            return

        logger.info("✅ Proceeding with analysis of available records.")

        # --- Apply Schema Casting ---
        logger.info("🔎 Identifying and converting columns based on schema...")
        df, report = enforce_schema(df)

        # Log schema mutation report
        logger.info("\n📜 Data Type Conversion Report:\n%s", report.to_string())

        # --- Data Inspection (Post-Casting) ---
        logger.info("📊 Updated Data Characteristics:")
        df.info()
        logger.info("\n📌 Summary Statistics:\n%s", df.describe().to_string())
        logger.info("\n🔹 Sample Records:\n%s", df.head(n=5).to_string())

        # --- Data Analysis ---
        logger.info("🔎 Running data quality check...")
        quality_report = check_data_quality(df)
        logger.info(f"Data Quality Report:\n{quality_report}")

        logger.info("📊 Computing summary statistics...")
        summary_stats = compute_summary_statistics(df)
        logger.info(f"Summary Statistics:\n{summary_stats}")

        logger.info("🔗 Computing correlations...")
        correlations = compute_correlations(df)
        logger.info(f"Correlation Matrix:\n{correlations}")

        # --- Data Visualization ---
        process_visualizations(df)

    except Exception as e:
        logger.error(f"❌ Error: {e}")


def log_data_preview(data):
    """Logs preview of datasets if available."""
    for key, value in data.items():
        preview = value.head() if value is not None else "Not available"
        logger.debug(f"📊 {key.upper()} Preview:\n{preview}")


def process_visualizations(df):
    """Handles visualization generation if numeric columns exist."""
    numeric_cols = df.select_dtypes(include=["number"]).columns

    if not numeric_cols.any():
        logger.warning("⚠️ No numeric columns found for visualization.")
        return

    logger.info("📈 Generating visualizations...")

    for col in numeric_cols[:3]:  # Limit to 3 columns for brevity
        logger.debug(f"Generating histogram for {col}...")
        plot_histogram(df, col)

        logger.debug(f"Generating boxplot for {col}...")
        plot_boxplot(df, col)

    logger.debug("Generating correlation heatmap...")
    plot_correlation_matrix(df)


# Register CLI commands
cli.add_command(analyze)

if __name__ == "__main__":
    cli()
