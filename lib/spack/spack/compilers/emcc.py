# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.compiler
from spack.version import ver


class Emcc(spack.compiler.Compiler):
    cc_names = ['emcc']
    cxx_names = ['em++']

    # Named wrapper links within build_env_path
    link_paths = {'cc': os.path.join('upstream', 'emscripten', 'emcc'),
                  'cxx': os.path.join('upstream', 'emscripten', 'em++'),
                  'f77': '',
                  'fc': ''}

    @property
    def verbose_flag(self):
        return "-v"

    @property
    def debug_flags(self):
        return ['-g', '-gsource-map', '-gseparate-dwarf', '-g0', '-g1', '-g2', '-g3']

    @property
    def opt_flags(self):
        return ['-O0', '-O1', '-O2', '-O3', '-Os', '-Oz']
