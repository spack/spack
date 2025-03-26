# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Alias names to convert legacy compilers to builtin packages and vice-versa"""

BUILTIN_TO_LEGACY_COMPILER = {
    "llvm": "clang",
    "intel-oneapi-compilers": "oneapi",
    "llvm-amdgpu": "rocmcc",
    "intel-oneapi-compiler-classic": "intel",
    "acfl": "arm",
}

LEGACY_COMPILER_TO_BUILTIN = {
    "clang": "llvm",
    "oneapi": "intel-oneapi-compilers",
    "rocmcc": "llvm-amdgpu",
    "intel": "intel-oneapi-compiler-classic",
    "arm": "acfl",
}
