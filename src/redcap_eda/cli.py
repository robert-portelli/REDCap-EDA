#!/usr/bin/env python3

import click
from redcap_eda.logger import set_log_level

"""
Command-line interface (CLI) for REDCap-EDA.
"""


@click.group()
@click.option("--debug", is_flag=True, help="Enable verbose debug logging")
def cli(debug):
    """REDCap-EDA: Perform Exploratory Data Analysis on REDCap datasets."""
    set_log_level(debug)


if __name__ == "__main__":
    cli()
