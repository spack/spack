# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwhich(Package):
    """
        Libwhich: the functionality of which for libraries.
    """

    homepage = "https://github.com/vtjnash/libwhich"
    url      = "https://github.com/vtjnash/libwhich.git"
    git      = "https://github.com/vtjnash/libwhich.git"

    version('master',  branch='master')
    maintainers = ['dmageeLANL']

    def install(self, spec, prefix):
        make()
        mkdir(prefix.bin)
        install('libwhich', prefix.bin)
