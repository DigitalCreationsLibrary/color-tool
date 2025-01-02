# SPDX-FileCopyrightText: 2024-present DigitalCreationsLibrary <aimosta.official@gmail.com>
#
# SPDX-License-Identifier: MIT
import click

from color_tool.__about__ import __version__
from color_tool.colorget import getColor



# @click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.group(context_settings={"help_option_names": ["-h", "--help"]},)
@click.version_option(version=__version__, prog_name="colo-tool")
def color_tool():
    pass
    
    
@color_tool.command()
def get():
    getColor()
    
