import os
import re
import multiprocessing
from version import Version

import tty
from utils import *
from spack.exception import *

# This lives in $prefix/lib/spac/spack/__file__
prefix = ancestor(__file__, 4)

# The spack script itself
spack_file = new_path(prefix, "bin", "spack")

# spack directory hierarchy
lib_path      = new_path(prefix, "lib", "spack")
env_path      = new_path(lib_path, "env")
module_path   = new_path(lib_path, "spack")
packages_path = new_path(module_path, "packages")

var_path      = new_path(prefix, "var", "spack")
stage_path    = new_path(var_path, "stage")

install_path  = new_path(prefix, "opt")

# Version information
spack_version = Version("0.1")

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", ""))

# Curl tool for fetching files.
curl = which("curl", required=True)

# Whether to build in tmp space or directly in the stage_path.
# If this is true, then spack will make stage directories in
# a tmp filesystem, and it will symlink them into stage_path.
use_tmp_stage = True

# Locations to use for staging and building, in order of preference
# Spack will try to create stage directories in <tmp_dir>/<username>
# if one of these tmp_dirs exists.  Otherwise it'll use a default
# location per the python implementation of tempfile.mkdtemp().
tmp_dirs = ['/nfs/tmp2', '/var/tmp', '/tmp']

# Important environment variables
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'
SPACK_LIB = 'SPACK_LIB'
SPACK_ENV_PATH = 'SPACK_ENV_PATH'
SPACK_DEPENDENCIES = 'SPACK_DEPENDENCIES'
SPACK_PREFIX = 'SPACK_PREFIX'
SPACK_BUILD_ROOT = 'SPACK_BUILD_ROOT'
