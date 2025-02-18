import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level
from redcap_eda.cast_schema import enforce_schema
from redcap_eda.analysis.eda import ExploratoryDataAnalysis


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose debug logging")
def cli(debug: bool) -> None:
    """Command-line interface for REDCap-EDA.

    This CLI tool loads REDCap datasets, applies schema casting,
    and performs exploratory data analysis.

    Args:
        debug (bool): Enables verbose logging if set.
    """
    set_log_level(debug)


@click.command()
@click.option(
    "--case",
    required=True,
    help="Specify the REDCap test case (e.g., 01, 07, 20)",
)
@click.option(
    "--output",
    default="eda_reports",
    help="Specify the directory to save reports",
)
def analyze(case: str, output: str) -> None:
    """Performs EDA on the specified REDCap test dataset.

    This function:
    - Loads dataset corresponding to the given test case.
    - Applies schema casting for strict data types.
    - Runs exploratory data analysis (EDA).
    - Saves visualizations and reports to the specified output directory.

    Args:
        case (str): The test case identifier (e.g., "01", "07", "20").
        output (str): The directory to store analysis reports.
    """
    logger.info(f"🔍 Loading Case {case}...")

    try:
        df = load_data()

        logger.info("✅ Proceeding with analysis of available records.")

        df, report = enforce_schema(df)
        logger.info("\n📜 Data Type Conversion Report:\n%s", report.to_string())

        # Run EDA with output directory
        eda = ExploratoryDataAnalysis(df, output_dir=output)
        eda_report = eda.explore()

        logger.debug("\n📜 EDA Report:\n%s", eda_report)

    except FileNotFoundError as e:
        logger.critical(f"❌ Dataset file not found: {e}")
    except ValueError as e:
        logger.warning(f"⚠️ Data integrity issue detected: {e}")
    except Exception as e:
        logger.exception(f"🚨 Unexpected error occurred: {e}")


@click.command()
def list_cases() -> None:
    """Lists available REDCap test cases."""
    logger.info("📂 Available test cases: ['01',]")


# Register CLI commands
cli.add_command(analyze)
cli.add_command(list_cases)

if __name__ == "__main__":
    cli()
