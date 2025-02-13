#!/usr/bin/env python3

"""
Command-line interface (CLI) for REDCap-EDA.
"""

import click


@click.group()
def cli():
    """REDCap-EDA: Perform Exploratory Data Analysis on REDCap datasets."""
    pass


if __name__ == "__main__":
    cli()
