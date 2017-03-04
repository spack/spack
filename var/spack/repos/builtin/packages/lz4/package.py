##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Lz4(Package):
    """LZ4 is lossless compression algorithm, providing compression speed
    at 400 MB/s per core, scalable with multi-cores CPU. It also features
    an extremely fast decoder, with speed in multiple GB/s per core,
    typically reaching RAM speed limits on multi-core systems."""

    homepage = "http://lz4.github.io/lz4/"
    url      = "https://github.com/lz4/lz4/archive/v1.7.5.tar.gz"

    version('1.7.5', 'c9610c5ce97eb431dddddf0073d919b9')
    version('1.3.1', '42b09fab42331da9d3fb33bd5c560de9')

    # depends_on('valgrind', type='test')

    def url_for_version(self, version):
        url = "https://github.com/lz4/lz4/archive"

        if version > Version('1.3.1'):
            return "{0}/v{1}.tar.gz".format(url, version)
        else:
            return "{0}/r{1}.tar.gz".format(url, version.joined)

    def install(self, spec, prefix):
        make()
        if self.run_tests:
            make('test')  # requires valgrind to be installed
        make('install', 'PREFIX={0}'.format(prefix))
