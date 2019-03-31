# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Lz4(Package):
    """LZ4 is lossless compression algorithm, providing compression speed
    at 400 MB/s per core, scalable with multi-cores CPU. It also features
    an extremely fast decoder, with speed in multiple GB/s per core,
    typically reaching RAM speed limits on multi-core systems."""

    homepage = "http://lz4.github.io/lz4/"
    url      = "https://github.com/lz4/lz4/archive/v1.7.5.tar.gz"

    version('1.8.3',   '33af5936ac06536805f9745e0b6d61da606a1f8b4cc5c04dd3cbaca3b9b4fc43')
    version('1.8.1.2', '343538e69ba752a386c669b1a28111e2')
    version('1.7.5',   'c9610c5ce97eb431dddddf0073d919b9')
    version('1.3.1',   '42b09fab42331da9d3fb33bd5c560de9')

    depends_on('valgrind', type='test')

    def url_for_version(self, version):
        url = "https://github.com/lz4/lz4/archive"

        if version > Version('1.3.1'):
            return "{0}/v{1}.tar.gz".format(url, version)
        else:
            return "{0}/r{1}.tar.gz".format(url, version.joined)

    def install(self, spec, prefix):
        if sys.platform != "darwin":
            make('MOREFLAGS=-lrt')  # fixes make error on CentOS6
        else:
            make()
        if self.run_tests:
            make('test')  # requires valgrind to be installed
        make('install', 'PREFIX={0}'.format(prefix))

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
