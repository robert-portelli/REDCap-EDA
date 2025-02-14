import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level
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
        data = {
            # "df_ui": load_data(case, "records"),
            "df_api": load_data(case, "records_api"),
        }

        # Log missing datasets
        missing_keys = [key for key, value in data.items() if value is None]
        if missing_keys:
            for key in missing_keys:
                logger.warning(f"⚠️ Case {case} is missing data from {key}")

        # Exit if all datasets are missing
        if all(value is None for value in data.values()):
            logger.error(f"❌ Case {case} lacks records for analysis.")
            return

        logger.info("✅ Proceeding with analysis of available records.")

        # Log dataset previews
        log_data_preview(data)

        # --- Data Analysis ---
        df_ui = data["df_ui"]  # Ensure df_ui is accessible in this scope
        logger.info("🔎 Running data quality check...")
        quality_report = check_data_quality(df_ui)
        logger.info(f"Data Quality Report:\n{quality_report}")

        logger.info("📊 Computing summary statistics...")
        summary_stats = compute_summary_statistics(df_ui)
        logger.info(f"Summary Statistics:\n{summary_stats}")

        logger.info("🔗 Computing correlations...")
        correlations = compute_correlations(df_ui)
        logger.info(f"Correlation Matrix:\n{correlations}")

        # --- Data Visualization ---
        process_visualizations(df_ui)

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
