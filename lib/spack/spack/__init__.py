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
import tempfile
from llnl.util.filesystem import *

# This lives in $prefix/lib/spack/spack/__file__
prefix = ancestor(__file__, 4)

# The spack script itself
spack_file = join_path(prefix, "bin", "spack")

# spack directory hierarchy
etc_path       = join_path(prefix, "etc")
lib_path       = join_path(prefix, "lib", "spack")
build_env_path = join_path(lib_path, "env")
module_path    = join_path(lib_path, "spack")
compilers_path = join_path(module_path, "compilers")
test_path      = join_path(module_path, "test")
hooks_path     = join_path(module_path, "hooks")
var_path       = join_path(prefix, "var", "spack")
stage_path     = join_path(var_path, "stage")
install_path   = join_path(prefix, "opt")
share_path     = join_path(prefix, "share", "spack")

#
# Set up the packages database.
#
from spack.packages import PackageDB
packages_path = join_path(var_path, "packages")
db = PackageDB(packages_path)

#
# Paths to mock files for testing.
#
mock_packages_path = join_path(var_path, "mock_packages")

mock_config_path = join_path(var_path, "mock_configs")
mock_site_config = join_path(mock_config_path, "site_spackconfig")
mock_user_config = join_path(mock_config_path, "user_spackconfig")

#
# This controls how spack lays out install prefixes and
# stage directories.
#
from spack.directory_layout import SpecHashDirectoryLayout
install_layout = SpecHashDirectoryLayout(install_path)

#
# PackageConfig parses the 'package' sections of .spackconfig, and
# can be used to determine spec sort orders
#
from spack.package_config import PackageConfig
pkgconfig = PackageConfig()

#
# This controls how things are concretized in spack.
# Replace it with a subclass if you want different
# policies.
#
from spack.concretize import DefaultConcretizer
concretizer = DefaultConcretizer()

# Version information
from spack.version import Version
spack_version = Version("0.8.15")

#
# Executables used by Spack
#
from spack.util.executable import Executable, which

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", "vi"))

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
tmp_dirs = []
_default_tmp = tempfile.gettempdir()
if _default_tmp != os.getcwd():
    tmp_dirs.append(os.path.join(_default_tmp, 'spack-stage'))
tmp_dirs.append('/nfs/tmp2/%u/spack-stage')

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
# When packages call 'from spack import *', this extra stuff is brought in.
#
# Spack internal code should call 'import spack' and accesses other
# variables (spack.db, paths, etc.) directly.
#
# TODO: maybe this should be separated out and should go in build_environment.py?
# TODO: it's not clear where all the stuff that needs to be included in packages
#       should live.  This file is overloaded for spack core vs. for packages.
#
__all__ = ['Package', 'Version', 'when', 'ver']
from spack.package import Package, ExtensionConflictError
from spack.version import Version, ver
from spack.multimethod import when

import llnl.util.filesystem
from llnl.util.filesystem import *
__all__ += llnl.util.filesystem.__all__

import spack.relations
from spack.relations import *
__all__ += spack.relations.__all__

import spack.util.executable
from spack.util.executable import *
__all__ += spack.util.executable.__all__
