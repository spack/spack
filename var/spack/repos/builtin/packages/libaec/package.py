# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libaec(CMakePackage):
    """Libaec provides fast lossless compression of 1 up to 32 bit wide signed
       or unsigned integers (samples). It implements Golomb-Rice compression
       method under the BSD license and includes a free drop-in replacement for
       the SZIP library.
    """

    homepage = 'https://gitlab.dkrz.de/k202009/libaec'
    url = 'https://gitlab.dkrz.de/api/v4/projects/k202009%2Flibaec/repository/archive.tar.gz?sha=v1.0.2'
    list_url = 'https://gitlab.dkrz.de/k202009/libaec/tags'

    provides('szip')

    version('1.0.2', '13fb9dca01f95e2794010312c8fe345a')
    version('1.0.1', '2180d2525d679a5f7950e7867b70e06b')
    version('1.0.0', 'ebc0b4e47fa4e1bd5783c2b1c960fe94')
