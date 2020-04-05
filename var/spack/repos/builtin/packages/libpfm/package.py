# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libpfm(Package):
    """ LibPFM4 is a helper library to program the performance monitoring events."""

    homepage = "https://github.com/wcohen/libpfm4"
    git      = "https://github.com/wcohen/libpfm4.git"
    maintainers = ['trahay']

    version('master',  branch='master')
    version('2020-03-09', commit='210b2ef95f33eccb671f2a88a979de5364c94465')

    def install(self, spec, prefix):
        env['PREFIX'] = prefix
        make('install')
