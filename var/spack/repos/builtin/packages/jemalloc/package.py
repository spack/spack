# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jemalloc(Package):
    """jemalloc is a general purpose malloc(3) implementation that emphasizes
       fragmentation avoidance and scalable concurrency support."""
    homepage = "http://www.canonware.com/jemalloc/"
    url      = "https://github.com/jemalloc/jemalloc/releases/download/4.0.4/jemalloc-4.0.4.tar.bz2"

    version('5.2.1', sha256='34330e5ce276099e2e8950d9335db5a875689a4c6a56751ef3b1d8c537f887f6')
    version('4.5.0', 'a5624318fbf5bf653697306642683a11')
    version('4.4.0', '81b59778e19696d99e2f7922820671b0')
    version('4.3.1', 'f204c0ea1aef92fbb339dc640de338a6')
    version('4.2.1', '094b0a7b8c77c464d0dc8f0643fd3901')
    version('4.2.0', 'e6b5d5a1ea93a04207528d274efdd144')
    version('4.1.0', 'c4e53c947905a533d5899e5cc3da1f94')
    version('4.0.4', '687c5cc53b9a7ab711ccd680351ff988')

    variant('stats', default=False, description='Enable heap statistics')
    variant('prof', default=False, description='Enable heap profiling')
    variant('je', default=False, description='Prepend the public API functions with "je_"')

    def install(self, spec, prefix):
        configure_args = ['--prefix=%s' % prefix, ]

        if '+stats' in spec:
            configure_args.append('--enable-stats')
        if '+prof' in spec:
            configure_args.append('--enable-prof')
        if '+je' in spec:
            configure_args.append('--with-jemalloc-prefix=je_')

        configure(*configure_args)

        # Don't use -Werror
        filter_file(r'-Werror=\S*', '', 'Makefile')

        make()
        make("install")
