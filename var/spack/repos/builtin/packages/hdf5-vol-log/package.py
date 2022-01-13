# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VolLog(AutotoolsPackage):
    """Log-based VOL - an HDF5 VOL Plugin that stores HDF5 datasets in a log-based
    storage layout."""

    homepage = 'https://github.com/DataLib-ECP/vol-log-based'
    url      = 'https://github.com/DataLib-ECP/vol-log-based'
    git = 'https://github.com/DataLib-ECP/vol-log-based.git'
    maintainers = ['hyoklee']

    version('master', commit='b13778efd9e0c79135a9d7352104985408078d45')

    depends_on('hdf5@1.12.1:')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    def configure_args(self):
        args = []

        args.append('--enable-shared')
        args.append('--enable-zlib')

        return args
