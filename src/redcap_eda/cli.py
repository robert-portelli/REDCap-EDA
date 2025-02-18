import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level
from redcap_eda.cast_schema import SchemaHandler
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
    "--sample",
    is_flag=True,
    help="Use the default REDCap sample dataset (Case 01).",
)
@click.option(
    "--csv",
    type=click.Path(exists=True),
    help="Path to a user-provided CSV file.",
)
@click.option(
    "--schema",
    type=click.Path(exists=True),
    help="Path to a schema file (JSON/YAML).",
)
@click.option(
    "--output",
    default="eda_reports",
    help="Specify the directory to save reports.",
)
def analyze(sample: bool, csv: str | None, schema: str | None, output: str) -> None:
    """Performs EDA on the specified dataset.

    Args:
        sample (bool): Use the predefined REDCap sample dataset.
        csv (str | None): Path to a user-provided dataset.
        schema (str | None): Path to a schema file.
        output (str): Directory to store analysis reports.
    """
    if csv and sample:
        logger.error("❌ Cannot specify both `--sample` and `--csv`. Choose one.")
        return

    if not csv and not sample:
        logger.info(
            "📊 No dataset specified, defaulting to REDCap test sample (Case 01).",
        )
        sample = True

    dataset_source = "Sample Dataset" if sample else csv
    logger.info(f"📂 Dataset source: {dataset_source}")

    try:
        # Load the dataset
        df = load_data(sample=sample, csv_path=csv)

        # Initialize SchemaHandler
        schema_handler = SchemaHandler(schema)

        # Handle schema enforcement
        schema_handler.load_or_create_schema(df, csv_path=csv or "")

        df, report = schema_handler.enforce_schema(df)

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
