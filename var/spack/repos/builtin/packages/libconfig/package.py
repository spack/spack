# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libconfig(AutotoolsPackage):
    """C/C++ Configuration File Library"""

    homepage = "http://www.hyperrealm.com/libconfig/"
    url      = "https://github.com/hyperrealm/libconfig/archive/v1.5.tar.gz"

    force_autoreconf = True
    # there is currently a build error with version 1.6, see:
    # https://github.com/hyperrealm/libconfig/issues/47
    # version('1.6', '2ccd24b6a2ee39f7ff8a3badfafb6539')
    version('1.5', 'e92a91c2ddf3bf77bea0f5ed7f09e492', preferred=True)

    depends_on('m4', type=('build'))
    depends_on('autoconf', type=('build'))
    depends_on('automake', type=('build'))
    depends_on('libtool', type=('build'))
