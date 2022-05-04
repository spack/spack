# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# flake8: noqa: F401
"""pkgkit is a set of useful build tools and directives for packages.

Everything in this module is automatically imported into Spack package files.
"""
import llnl.util.filesystem
from llnl.util.filesystem import *

import spack.directives
import spack.util.executable
from spack.build_systems.aspell_dict import AspellDictPackage
from spack.build_systems.autotools import AutotoolsPackage, autotools
from spack.build_systems.bundle import BundlePackage
from spack.build_systems.cached_cmake import (
    CachedCMakePackage,
    cmake_cache_option,
    cmake_cache_path,
    cmake_cache_string,
)
from spack.build_systems.cmake import CMakePackage
from spack.build_systems.cuda import CudaPackage
from spack.build_systems.generic import Package, generic
from spack.build_systems.gnu import GNUMirrorPackage
from spack.build_systems.intel import IntelPackage
from spack.build_systems.lua import LuaPackage
from spack.build_systems.makefile import MakefilePackage
from spack.build_systems.maven import MavenPackage
from spack.build_systems.meson import MesonPackage
from spack.build_systems.octave import OctavePackage
from spack.build_systems.oneapi import (
    IntelOneApiLibraryPackage,
    IntelOneApiPackage,
    IntelOneApiStaticLibraryList,
)
from spack.build_systems.perl import PerlPackage
from spack.build_systems.python import PythonExtension, PythonPackage
from spack.build_systems.qmake import QMakePackage
from spack.build_systems.r import RPackage
from spack.build_systems.racket import RacketPackage
from spack.build_systems.rocm import ROCmPackage
from spack.build_systems.ruby import RubyPackage
from spack.build_systems.scons import SConsPackage
from spack.build_systems.sip import SIPPackage
from spack.build_systems.sourceforge import SourceforgePackage
from spack.build_systems.sourceware import SourcewarePackage
from spack.build_systems.waf import WafPackage
from spack.build_systems.xorg import XorgPackage
from spack.dependency import all_deptypes
from spack.directives import *
from spack.install_test import get_escaped_text_output
from spack.installer import (
    ExternalPackageError,
    InstallError,
    InstallLockError,
    UpstreamPackageError,
)
from spack.mixins import filter_compiler_wrappers
from spack.multimethod import when
from spack.package import (
    DependencyConflictError,
    build_system_flags,
    env_flags,
    flatten_dependencies,
    inject_flags,
    install_dependency_symlinks,
    on_package_attributes,
    run_after,
    run_before,
)
from spack.spec import InvalidSpecDetected, Spec
from spack.util.executable import *
from spack.variant import (
    any_combination_of,
    auto_or_any_combination_of,
    conditional,
    disjoint_sets,
)
from spack.version import Version, ver
