# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cub(Package):
    """CUB is a C++ header library of cooperative threadblock primitives
    and other utilities for CUDA kernel programming."""

    homepage = "https://nvlabs.github.com/cub"
    url      = "https://github.com/NVlabs/cub/archive/1.6.4.zip"

    version('1.7.1', '028ac43922a4538596338ad5aef0f0c4')
    version('1.6.4', '924fc12c0efb17264c3ad2d611ed1c51')
    version('1.4.1', '74a36eb84e5b5f0bf54aa3df39f660b2')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree('cub', join_path(prefix.include, 'cub'))
