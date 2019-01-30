# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxstream(Package):
    '''LIBXSTREAM is a library to work with streams, events, and code regions
    that are able to run asynchronous while preserving the usual stream
    conditions.'''

    homepage = 'https://github.com/hfp/libxstream'
    url      = 'https://github.com/hfp/libxstream/archive/0.9.0.tar.gz'

    version('0.9.0', 'fd74b7cf5f145ff4925d91be2809571c')

    def patch(self):
        kwargs = {'ignore_absent': False, 'backup': True, 'string': True}
        makefile = FileFilter('Makefile.inc')

        makefile.filter('CC =',  'CC ?=',  **kwargs)
        makefile.filter('CXX =', 'CXX ?=', **kwargs)
        makefile.filter('FC =',  'FC ?=',  **kwargs)

    def install(self, spec, prefix):
        make()
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('documentation', prefix.share + '/libxstream/doc/')
