# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module re-exports symbols that are part of the v1.0 Package API, but were removed in the
v2.0 Package API after build systems were moved into the ``spack_repo.builtin`` package.
In older versions of Spack, these symbols were re-exported from ``spack.package``."""

from .aspell_dict import AspellDictPackage
from .autotools import AutotoolsPackage
from .bundle import BundlePackage
from .cached_cmake import (
    CachedCMakePackage,
    cmake_cache_filepath,
    cmake_cache_option,
    cmake_cache_path,
    cmake_cache_string,
)
from .cargo import CargoPackage
from .cmake import CMakePackage, generator
from .compiler import CompilerPackage
from .cuda import CudaPackage
from .generic import Package
from .gnu import GNUMirrorPackage
from .go import GoPackage
from .lua import LuaPackage
from .makefile import MakefilePackage
from .maven import MavenPackage
from .meson import MesonPackage
from .msbuild import MSBuildPackage
from .nmake import NMakePackage
from .octave import OctavePackage
from .oneapi import (
    INTEL_MATH_LIBRARIES,
    IntelOneApiLibraryPackage,
    IntelOneApiLibraryPackageWithSdk,
    IntelOneApiPackage,
    IntelOneApiStaticLibraryList,
)
from .perl import PerlPackage
from .python import PythonExtension, PythonPackage
from .qmake import QMakePackage
from .r import RPackage
from .racket import RacketPackage
from .rocm import ROCmPackage
from .ruby import RubyPackage
from .scons import SConsPackage
from .sip import SIPPackage
from .sourceforge import SourceforgePackage
from .sourceware import SourcewarePackage
from .waf import WafPackage
from .xorg import XorgPackage

__all__ = [
    "AspellDictPackage",
    "AutotoolsPackage",
    "BundlePackage",
    "CachedCMakePackage",
    "cmake_cache_filepath",
    "cmake_cache_option",
    "cmake_cache_path",
    "cmake_cache_string",
    "CargoPackage",
    "CMakePackage",
    "generator",
    "CompilerPackage",
    "CudaPackage",
    "Package",
    "GNUMirrorPackage",
    "GoPackage",
    "IntelOneApiLibraryPackageWithSdk",
    "IntelOneApiLibraryPackage",
    "IntelOneApiStaticLibraryList",
    "IntelOneApiPackage",
    "INTEL_MATH_LIBRARIES",
    "LuaPackage",
    "MakefilePackage",
    "MavenPackage",
    "MesonPackage",
    "MSBuildPackage",
    "NMakePackage",
    "OctavePackage",
    "PerlPackage",
    "PythonExtension",
    "PythonPackage",
    "QMakePackage",
    "RacketPackage",
    "RPackage",
    "ROCmPackage",
    "RubyPackage",
    "SConsPackage",
    "SIPPackage",
    "SourceforgePackage",
    "SourcewarePackage",
    "WafPackage",
    "XorgPackage",
]
