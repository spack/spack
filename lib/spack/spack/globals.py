##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os

from llnl.util.filesystem import *

from spack.version import Version
from spack.util.executable import *
from spack.directory_layout import SpecHashDirectoryLayout
from spack.concretize import DefaultConcretizer
from spack.packages import PackageDB

# This lives in $prefix/lib/spac/spack/__file__
prefix = ancestor(__file__, 4)

# The spack script itself
spack_file = join_path(prefix, "bin", "spack")

# spack directory hierarchy
lib_path       = join_path(prefix, "lib", "spack")
env_path       = join_path(lib_path, "env")
module_path    = join_path(lib_path, "spack")
compilers_path = join_path(module_path, "compilers")
test_path      = join_path(module_path, "test")

var_path       = join_path(prefix, "var", "spack")
stage_path     = join_path(var_path, "stage")

install_path   = join_path(prefix, "opt")

#
# Set up the packages database.
#
db = PackageDB(join_path(module_path, "packages"))


#
# This controls how spack lays out install prefixes and
# stage directories.
#
install_layout = SpecHashDirectoryLayout(install_path, prefix_size=6)

#
# This controls how things are concretized in spack.
# Replace it with a subclass if you want different
# policies.
#
concretizer = DefaultConcretizer()

# Version information
spack_version = Version("1.0")

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", ""))

# Curl tool for fetching files.
curl = which("curl", required=True)

# Whether to build in tmp space or directly in the stage_path.
# If this is true, then spack will make stage directories in
# a tmp filesystem, and it will symlink them into stage_path.
use_tmp_stage = True

# Locations to use for staging and building, in order of preference
# Use a %u to add a username to the stage paths here, in case this
# is a shared filesystem.  Spack will use the first of these paths
# that it can create.
tmp_dirs = ['/nfs/tmp2/%u/spack-stage',
            '/var/tmp/%u/spack-stage',
            '/tmp/%u/spack-stage']

# Whether spack should allow installation of unsafe versions of
# software.  "Unsafe" versions are ones it doesn't have a checksum
# for.
do_checksum = True

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

#
# Places to download tarballs from.  Examples:
#
# For a local directory:
#   mirrors = ['file:///Users/gamblin2/spack-mirror']
#
# For a website:
#   mirrors = ['http://spackports.org/spack-mirror/']
#
# For no mirrors:
#   mirrors = []
#
mirrors = []

# Important environment variables
SPACK_NO_PARALLEL_MAKE = 'SPACK_NO_PARALLEL_MAKE'
SPACK_LIB = 'SPACK_LIB'
SPACK_ENV_PATH = 'SPACK_ENV_PATH'
SPACK_DEPENDENCIES = 'SPACK_DEPENDENCIES'
SPACK_PREFIX = 'SPACK_PREFIX'
SPACK_BUILD_ROOT = 'SPACK_BUILD_ROOT'
