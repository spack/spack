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

#: major, minor, patch version for Spack, in a tuple
spack_version_info = (0, 11, 2)

#: String containing Spack version joined with .'s
spack_version = '.'.join(str(v) for v in spack_version_info)


#-----------------------------------------------------------------------------
# When packages call 'from spack import *', we import a set of things that
# should be useful for builds.
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
