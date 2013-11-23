import os

import spack.arch as arch
from spack.version import Version
from spack.util.filesystem import *
from spack.util.executable import *
from spack.directory_layout import DefaultDirectoryLayout
from spack.concretize import DefaultConcretizer

# This lives in $prefix/lib/spac/spack/__file__
prefix = ancestor(__file__, 4)

# The spack script itself
spack_file = new_path(prefix, "bin", "spack")

# spack directory hierarchy
lib_path       = new_path(prefix, "lib", "spack")
env_path       = new_path(lib_path, "env")
module_path    = new_path(lib_path, "spack")
packages_path  = new_path(module_path, "packages")
compilers_path = new_path(module_path, "compilers")
test_path      = new_path(module_path, "test")

var_path       = new_path(prefix, "var", "spack")
stage_path     = new_path(var_path, "stage")

install_path   = new_path(prefix, "opt")

#
# This controls how spack lays out install prefixes and
# stage directories.
#
install_layout = DefaultDirectoryLayout(install_path)

#
# This controls how things are concretized in spack.
# Replace it with a subclass if you want different
# policies.
#
concretizer = DefaultConcretizer()

# Version information
spack_version = Version("0.5")

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

#
# SYS_TYPE to use for the spack installation.
# Value of this determines what platform spack thinks it is by
# default.  You can assign three types of values:
# 1. None
#    Spack will try to determine the sys_type automatically.
#
# 2. A string
#    Spack will assume that the sys_type is hardcoded to the value.
#
# 3. A function that returns a string:
#    Spack will use this function to determine the sys_type.
#
sys_type = None

# Important environment variables
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'
SPACK_LIB = 'SPACK_LIB'
SPACK_ENV_PATH = 'SPACK_ENV_PATH'
SPACK_DEPENDENCIES = 'SPACK_DEPENDENCIES'
SPACK_PREFIX = 'SPACK_PREFIX'
SPACK_BUILD_ROOT = 'SPACK_BUILD_ROOT'
