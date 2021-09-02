# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Systemc(CMakePackage):
    """SystemC: System level modeling, design exploration, performance modeling, and more."""

    homepage = "https://www.accellera.org/downloads/standards/systemc"
    url      = "https://accellera.org/images/downloads/standards/systemc/systemc-2.3.3.tar.gz"

    maintainers = ['nicmcd']

    version('2.3.3', sha256='5781b9a351e5afedabc37d145e5f7edec08f3fd5de00ffeb8fa1f3086b1f7b3f')
