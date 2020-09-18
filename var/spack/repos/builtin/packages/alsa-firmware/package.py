# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AlsaFirmware(AutotoolsPackage):
    """The Advanced Linux Sound Architecture (ALSA) - firmware"""

    homepage = "https://github.com/alsa-project/alsa-firmware"
    url      = "https://github.com/alsa-project/alsa-firmware/archive/v1.2.1.tar.gz"

    version('1.2.1',  sha256='d7a54018a35d34d35963363c29403d9f2ea57e74414b78ba76ee053e5e04000f')
    version('1.0.29', sha256='c07fef3fe1344981ec47ca29891b4625e86f51fea7983e056db217d742caa7bf')
    version('1.0.28', sha256='084cbb7b5f8e568e3a3e97ddce5bff8a6246afcd4bcacf436d67450e90a4ab99')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
