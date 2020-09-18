# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Addrwatch(AutotoolsPackage):
    """A tool similar to arpwatch for IPv4/IPv6 and ethernet address
    pairing monitoring."""

    homepage = "https://github.com/fln/addrwatch"
    url      = "https://github.com/fln/addrwatch/archive/v1.0.2.tar.gz"

    version('1.0.2', sha256='56a2180305e95adde584bd9502771269b9a216419b49631046b368502d5d5fba')
    version('1.0.1', sha256='f772b62b1c6570b577473e7c98614dad1124352b377324cbebb36360d8f4ce5a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('libevent')
    depends_on('libpcap')
