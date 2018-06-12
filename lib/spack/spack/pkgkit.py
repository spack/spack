# flake8: noqa: F401
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
"""pkgkit is a set of useful build tools and directives for packages.

Everything in this module is automatically imported into Spack package files.
"""
import llnl.util.filesystem
from llnl.util.filesystem import *

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
from spack.build_systems.meson import MesonPackage

from spack.mixins import filter_compiler_wrappers

from spack.version import Version, ver

from spack.spec import Spec

from spack.dependency import all_deptypes

from spack.multimethod import when

import spack.directives
from spack.directives import *

import spack.util.executable
from spack.util.executable import *

from spack.package import \
    install_dependency_symlinks, flatten_dependencies, \
    DependencyConflictError, InstallError, ExternalPackageError
