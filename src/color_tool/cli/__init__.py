# SPDX-FileCopyrightText: 2024-present DigitalCreationsLibrary <aimosta.official@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from color_tool.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="color tool")
def color_tool():
    click.echo("Hello world!")
