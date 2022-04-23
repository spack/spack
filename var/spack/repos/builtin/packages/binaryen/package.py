# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

from spack import *


class Binaryen(CMakePackage):
    """Compiler infrastructure and toolchain library for WebAssembly"""

    homepage = "https://github.com/WebAssembly/binaryen"
    git      = "https://github.com/WebAssembly/binaryen.git"
    url      = "https://github.com/WebAssembly/binaryen/archive/refs/tags/version_105.tar.gz"

    version('105', sha256='c5ec27c157d3b33ce4360607cc6afe565fa490094237895db2162b3a7d667da2')

    executables = [
        'wasm-opt',
        'wasm-as',
        'wasm-dis',
        'wasm2js',
        'wasm-reduce',
        'wasm-shell',
        'wasm-emscripten-finalize',
        'wasm-ctor-eval',
        'binaryen.js',
    ]
