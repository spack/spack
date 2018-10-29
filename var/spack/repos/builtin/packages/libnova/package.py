# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnova(AutotoolsPackage):
    """"libnova is a general purpose, double precision, Celestial Mechanics,
        Astrometry and Astrodynamics library."""

    homepage = "http://libnova.sourceforge.net"
    url      = "https://sourceforge.net/projects/libnova/files/libnova/v%200.15.0/libnova-0.15.0.tar.gz/download"

    version('0.15.0', '756fdb55745cb78511f83a62c25f3be4')

    depends_on('m4')
    depends_on('autoconf')
    depends_on('automake')
    depends_on('libtool')

    force_autoreconf = True
