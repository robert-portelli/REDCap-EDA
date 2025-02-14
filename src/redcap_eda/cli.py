import click
from redcap_eda.load_case_data import load_data
from redcap_eda.logger import logger, set_log_level


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
        df_ui = load_data(case, "records")
        df_api = load_data(case, "records_api")

        logger.debug(
            f"📊 Dataset Records UI: {df_ui.head() if df_ui is not None else 'Not available'}",
        )
        logger.debug(
            f"📊 Dataset Records API: {df_api.head() if df_api is not None else 'Not available'}",
        )

    except Exception as e:
        logger.error(f"❌ Error: {e}")


# Register CLI commands
cli.add_command(analyze)

if __name__ == "__main__":
    cli()
