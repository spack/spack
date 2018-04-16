# flake8: noqa
##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import sys
import multiprocessing

#-----------------------------------------------------------------------------
# Below code imports spack packages.
#-----------------------------------------------------------------------------
# The imports depend on paths above, or on each other, so ordering is tricky.
# TODO: refactor everything below to be more init order agnostic.


#-----------------------------------------------------------------------------
# Import spack.config first, as other modules may rely on its options.
# TODO: Below code should not import modules other than spack.config
#-----------------------------------------------------------------------------
import spack.config


# TODO: get this out of __init__.py
binary_cache_retrieved_specs = set()


#: The number of jobs to use when building in parallel.
#: By default, use all cores on the machine.
build_jobs = spack.config.get('config:build_jobs', multiprocessing.cpu_count())


#-----------------------------------------------------------------------------
# Initialize various data structures & objects at the core of Spack.
#
# TODO: move all of these imports out of __init__ to avoid importing the whole
# TODO: world on Spack startup. There are some design changes that need to be
# TODO: made to enable this (decoupling Spec, repo, DB, and store state).
#
# TODO: Spack probably needs some kind of object to manage this state so that
# TODO: this stuff doesn't have to be at module scope.
# -----------------------------------------------------------------------------
# Version information
from spack.version import Version
spack_version = Version("0.11.2")


# Set up the default packages database.
import spack.error
try:
    import spack.repository
    repo = spack.repository.RepoPath()
    sys.meta_path.append(repo)
except spack.error.SpackError as e:
    import llnl.util.tty as tty
    tty.die('while initializing Spack RepoPath:', e.message)


#: Concretizer class implements policy decisions for concretization
from spack.concretize import Concretizer
concretizer = Concretizer()


#: Needed for test dependencies
from spack.package_prefs import PackageTesting
package_testing = PackageTesting()


#-----------------------------------------------------------------------------
# When packages call 'from spack import *', we import a set of things that
# should be useful for builds.
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
from spack.build_systems.aspell_dict import AspellDictPackage
from spack.build_systems.autotools import AutotoolsPackage
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.cuda import CudaPackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.octave import OctavePackage
from spack.build_systems.python import PythonPackage
from spack.build_systems.r import RPackage
from spack.build_systems.perl import PerlPackage
from spack.build_systems.intel import IntelPackage

__all__ += [
    'run_before',
    'run_after',
    'on_package_attributes',
    'Package',
    'MakefilePackage',
    'AspellDictPackage',
    'AutotoolsPackage',
    'CMakePackage',
    'CudaPackage',
    'QMakePackage',
    'SConsPackage',
    'WafPackage',
    'OctavePackage',
    'PythonPackage',
    'RPackage',
    'PerlPackage',
    'IntelPackage',
]

from spack.mixins import filter_compiler_wrappers
__all__ += ['filter_compiler_wrappers']

from spack.version import Version, ver
__all__ += ['Version', 'ver']

from spack.spec import Spec
__all__ += ['Spec']

from spack.dependency import all_deptypes
__all__ += ['all_deptypes']

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

from spack.package import \
    install_dependency_symlinks, flatten_dependencies, \
    DependencyConflictError, InstallError, ExternalPackageError
__all__ += [
    'install_dependency_symlinks', 'flatten_dependencies',
    'DependencyConflictError', 'InstallError', 'ExternalPackageError']

# Add default values for attributes that would otherwise be modified from
# Spack main script
debug = False
