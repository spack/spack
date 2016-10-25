# flake8: noqa
##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import sys
import tempfile
import getpass
from llnl.util.filesystem import *
import llnl.util.tty as tty

# This lives in $prefix/lib/spack/spack/__file__
spack_root = ancestor(__file__, 4)

# The spack script itself
spack_file = join_path(spack_root, "bin", "spack")

# spack directory hierarchy
lib_path       = join_path(spack_root, "lib", "spack")
build_env_path = join_path(lib_path, "env")
module_path    = join_path(lib_path, "spack")
platform_path  = join_path(module_path, 'platforms')
compilers_path = join_path(module_path, "compilers")
operating_system_path = join_path(module_path, 'operating_systems')
test_path      = join_path(module_path, "test")
hooks_path     = join_path(module_path, "hooks")
var_path       = join_path(spack_root, "var", "spack")
stage_path     = join_path(var_path, "stage")
repos_path     = join_path(var_path, "repos")
share_path     = join_path(spack_root, "share", "spack")
cache_path     = join_path(var_path, "cache")

# User configuration location
user_config_path = os.path.expanduser('~/.spack')

import spack.fetch_strategy
fetch_cache = spack.fetch_strategy.FsCache(cache_path)

from spack.file_cache import FileCache
user_cache_path = join_path(user_config_path, 'cache')
user_cache = FileCache(user_cache_path)

prefix = spack_root
opt_path       = join_path(prefix, "opt")
install_path   = join_path(opt_path, "spack")
etc_path       = join_path(prefix, "etc")

#
# Set up the default packages database.
#
import spack.repository
try:
    repo = spack.repository.RepoPath()
    sys.meta_path.append(repo)
except spack.error.SpackError, e:
    tty.die('while initializing Spack RepoPath:', e.message)

#
# Set up the installed packages database
#
from spack.database import Database
installed_db = Database(install_path)

#
# Paths to built-in Spack repositories.
#
packages_path      = join_path(repos_path, "builtin")
mock_packages_path = join_path(repos_path, "builtin.mock")

#
# This controls how spack lays out install prefixes and
# stage directories.
#
from spack.directory_layout import YamlDirectoryLayout
install_layout = YamlDirectoryLayout(install_path)

#
# This controls how packages are sorted when trying to choose
# the most preferred package.  More preferred packages are sorted
# first.
#
from spack.preferred_packages import PreferredPackages
pkgsort = PreferredPackages()

#
# This tests ABI compatibility between packages
#
from spack.abi import ABI
abi = ABI()

#
# This controls how things are concretized in spack.
# Replace it with a subclass if you want different
# policies.
#
from spack.concretize import DefaultConcretizer
concretizer = DefaultConcretizer()

# Version information
from spack.version import Version
spack_version = Version("0.9.1")

#
# Executables used by Spack
#
from spack.util.executable import Executable, which

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", "vi"))

# If this is enabled, tools that use SSL should not verify
# certifiates. e.g., curl should use the -k option.
insecure = False

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
_tmp_user = getpass.getuser()

_tmp_candidates = (_default_tmp, '/nfs/tmp2', '/tmp', '/var/tmp')
for path in _tmp_candidates:
    # don't add a second username if it's already unique by user.
    if _tmp_user not in path:
        tmp_dirs.append(join_path(path, '%u', 'spack-stage'))
    else:
        tmp_dirs.append(join_path(path, 'spack-stage'))

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
# variables (spack.repo, paths, etc.) directly.
#
# TODO: maybe this should be separated out to build_environment.py?
# TODO: it's not clear where all the stuff that needs to be included in
#       packages should live.  This file is overloaded for spack core vs.
#       for packages.
#
__all__ = ['Package',
           'CMakePackage',
           'AutotoolsPackage',
           'MakefilePackage',
           'Version',
           'when',
           'ver',
           'alldeps',
           'nolink']
from spack.package import Package, ExtensionConflictError
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.version import Version, ver
from spack.spec import DependencySpec, alldeps, nolink
from spack.multimethod import when

import llnl.util.filesystem
from llnl.util.filesystem import *
__all__ += llnl.util.filesystem.__all__

import spack.directives
from spack.directives import *
__all__ += spack.directives.__all__

import spack.util.executable
from spack.util.executable import *
__all__ += spack.util.executable.__all__

from spack.package import \
    install_dependency_symlinks, flatten_dependencies, \
    DependencyConflictError, InstallError, ExternalPackageError
__all__ += [
    'install_dependency_symlinks', 'flatten_dependencies',
    'DependencyConflictError', 'InstallError', 'ExternalPackageError']
