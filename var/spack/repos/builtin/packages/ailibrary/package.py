# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ailibrary(Package):
    """AiLibrary is a single-header C++ Library from Ailurus Studio that brings you extra time to admire life instead of coding the same functions again and again."""

    homepage = "https://github.com/starobinskii/AiLibrary"
    url      = "https://github.com/starobinskii/AiLibrary/archive/v1.3.0.tar.gz"

    version('1.3.0', '56f59bbacfc242f9b8b38d9f2b8133ec')

    sanity_check_is_file = ['include/ai.hh']
    sanity_check_is_file = ['include/ai']

    def install(self, spec, prefix):
        make()
        mkdir(prefix.include)
        filter_file(r'/usr/local', prefix, 'Makefile')
        make("install")
