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

#-----------------------------------------------------------------------------
# Variables describing how Spack is laid out in its prefix.
#-----------------------------------------------------------------------------
# This file lives in $prefix/lib/spack/spack/__file__
spack_root = ancestor(__file__, 4)

# The spack script itself
spack_file = join_path(spack_root, "bin", "spack")

# spack directory hierarchy
lib_path       = join_path(spack_root, "lib", "spack")
external_path  = join_path(lib_path, "external")
build_env_path = join_path(lib_path, "env")
module_path    = join_path(lib_path, "spack")
platform_path  = join_path(module_path, 'platforms')
compilers_path = join_path(module_path, "compilers")
build_systems_path = join_path(module_path, 'build_systems')
operating_system_path = join_path(module_path, 'operating_systems')
test_path      = join_path(module_path, "test")
hooks_path     = join_path(module_path, "hooks")
var_path       = join_path(spack_root, "var", "spack")
stage_path     = join_path(var_path, "stage")
repos_path     = join_path(var_path, "repos")
share_path     = join_path(spack_root, "share", "spack")

# Paths to built-in Spack repositories.
packages_path      = join_path(repos_path, "builtin")
mock_packages_path = join_path(repos_path, "builtin.mock")

# User configuration location
user_config_path = os.path.expanduser('~/.spack')

prefix = spack_root
opt_path       = join_path(prefix, "opt")
etc_path       = join_path(prefix, "etc")


#-----------------------------------------------------------------------------
# Initial imports (only for use in this file -- see __all__ below.)
#-----------------------------------------------------------------------------
# These imports depend on the paths above, or on each other
# Group them here so it's easy to understand the order.
# TODO: refactor this stuff to be more init order agnostic.
import spack.repository
import spack.error
import spack.config
import spack.fetch_strategy
from spack.file_cache import FileCache
from spack.package_prefs import PreferredPackages
from spack.abi import ABI
from spack.concretize import DefaultConcretizer
from spack.version import Version
from spack.util.path import canonicalize_path


#-----------------------------------------------------------------------------
# Initialize various data structures & objects at the core of Spack.
#-----------------------------------------------------------------------------
# Version information
spack_version = Version("0.10.0")


# Set up the default packages database.
try:
    repo = spack.repository.RepoPath()
    sys.meta_path.append(repo)
except spack.error.SpackError, e:
    tty.die('while initializing Spack RepoPath:', e.message)


# Tests ABI compatibility between packages
abi = ABI()


# This controls how things are concretized in spack.
# Replace it with a subclass if you want different
# policies.
concretizer = DefaultConcretizer()

#-----------------------------------------------------------------------------
# config.yaml options
#-----------------------------------------------------------------------------
_config = spack.config.get_config('config')


# Path where downloaded source code is cached
cache_path = canonicalize_path(
    _config.get('source_cache', join_path(var_path, "cache")))
fetch_cache = spack.fetch_strategy.FsCache(cache_path)


# cache for miscellaneous stuff.
misc_cache_path = canonicalize_path(
    _config.get('misc_cache', join_path(user_config_path, 'cache')))
misc_cache = FileCache(misc_cache_path)


# If this is enabled, tools that use SSL should not verify
# certifiates. e.g., curl should use the -k option.
insecure = not _config.get('verify_ssl', True)


# Whether spack should allow installation of unsafe versions of software.
# "Unsafe" versions are ones it doesn't have a checksum for.
do_checksum = _config.get('checksum', True)


# If this is True, spack will not clean the environment to remove
# potentially harmful variables before builds.
dirty = _config.get('dirty', False)


#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------
__all__ = []

from spack.package import Package, run_before, run_after, on_package_attributes
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.r import RPackage

__all__ += [
    'run_before',
    'run_after',
    'on_package_attributes',
    'Package',
    'CMakePackage',
    'AutotoolsPackage',
    'MakefilePackage',
    'PythonPackage',
    'RPackage'
]

from spack.version import Version, ver
__all__ += ['Version', 'ver']

from spack.spec import Spec, alldeps
__all__ += ['Spec', 'alldeps']

from spack.multimethod import when
__all__ += ['when']

import llnl.util.filesystem
from llnl.util.filesystem import *
__all__ += llnl.util.filesystem.__all__

import spack.directives
from spack.directives import *
__all__ += spack.directives.__all__

import spack.util.executable
from spack.util.executable import *
__all__ += spack.util.executable.__all__

# User's editor from the environment
editor = Executable(os.environ.get("EDITOR", "vi"))

from spack.package import \
    install_dependency_symlinks, flatten_dependencies, \
    DependencyConflictError, InstallError, ExternalPackageError
__all__ += [
    'install_dependency_symlinks', 'flatten_dependencies',
    'DependencyConflictError', 'InstallError', 'ExternalPackageError']

# Add default values for attributes that would otherwise be modified from
# Spack main script
debug = True
spack_working_dir = None
