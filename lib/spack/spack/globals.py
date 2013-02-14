import os
import re
import multiprocessing
from version import Version

import tty
from fileutils import *

# This lives in $prefix/lib/spac/spack/__file__
prefix = ancestor(__file__, 4)

# The spack script itself
spack_file = new_path(prefix, "bin", "spack")

# spack directory hierarchy
lib_path      = new_path(prefix, "lib", "spack")
module_path   = new_path(lib_path, "spack")
packages_path = new_path(module_path, "packages")

var_path      = new_path(prefix, "var", "spack")
stage_path    = new_path(var_path, "stage")

install_path  = new_path(prefix, "opt")

# Version information
version = Version("0.1")

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", ""))

# Curl tool for fetching files.
curl = which("curl")
if not curl:
    tty.die("spack requires curl.  Make sure it is in your path.")

make = which("make")
make.add_default_arg("-j%d" % multiprocessing.cpu_count())
if not make:
    tty.die("spack requires make.  Make sure it is in your path.")

verbose = False
debug = False
