# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Metaphysicl(AutotoolsPackage):
    """Metaprogramming and operator-overloaded classes for
       numerical simulations."""
    homepage = "https://github.com/roystgnr/MetaPhysicL"
    url      = "https://github.com/roystgnr/MetaPhysicL/archive/v0.2.0.tar.gz"

    version('0.2.0', '2af65536524a3945b6507a30233ca1cf')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
