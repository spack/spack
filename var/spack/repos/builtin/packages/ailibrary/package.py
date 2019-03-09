# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ailibrary(Package):
    """AiLibrary is a single-header C++ Library from Ailurus Studio
    that brings you extra time to admire life instead of coding the
    same functions again and again
    """

    homepage = "https://github.com/starobinskii/AiLibrary"
    url      = "https://github.com/starobinskii/AiLibrary/archive/v1.3.0.tar.gz"

    version('1.3.0', 'f8da497ab2a81667b86d480d451d767bdf38bacea1ff606e404e314b503fdf8f')

    sanity_check_is_file = ['include/ai.hh']

    def install(self, spec, prefix):
        make()
        mkdir(prefix.include)
        filter_file(r'/usr/local', prefix, 'Makefile')
        make("install")
