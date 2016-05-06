__author__ = "Benedikt Hegner (CERN)"

import spack
import re

import llnl.util.tty as tty
from llnl.util.filesystem import *

#
# Read in the config
#
import spack.config
config = spack.config.get_config("install")

#
# Set up the install path
#
path = re.sub(r'^\$spack', spack.prefix, config['path'])

#
# Set up the installed packages database
#
from spack.database import Database
db = Database(path)

#
# This controls how spack lays out install prefixes and
# stage directories.
#
import spack.directory_layout

try:
    layout_name = config["layout"]
    layout_class = getattr(spack.directory_layout,layout_name)
    layout = layout_class(path)
except:
     tty.die("Invalid install directory layout %s chosen." %layout_name)

#
# Set up which loader lookup should be used in the build artifacts
#
loader_options = ["rpath","runpath"]
loader_lookup = config["loader_lookup"]
if loader_lookup not in loader_options:
    tty.die("Invalid loader lookup option %s chosen. Only %s supported." %(loader_lookup, loader_options))
