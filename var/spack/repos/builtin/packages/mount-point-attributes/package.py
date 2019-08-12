# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MountPointAttributes(AutotoolsPackage):
    """Library to turn expensive, non-scalable file system calls into simple
       string comparison operations."""

    homepage = "https://github.com/LLNL/MountPointAttributes"
    url = 'https://github.com/LLNL/MountPointAttributes/files/2270601/mountpointattr-1.1.tar.gz'

    version('1.1', 'c9f0e7f5a3e16b9a022e5948712ecb2a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    patch('mpa_type_conversion.patch', when='@1.1')
