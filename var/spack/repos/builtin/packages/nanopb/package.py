# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nanopb(CMakePackage):
    """Nanopb is a small code-size Protocol Buffers implementation
    in ansi C."""

    homepage = "https://jpa.kapsi.fi/nanopb/"
    url      = "https://github.com/nanopb/nanopb/archive/0.3.9.1.tar.gz"

    version('0.3.9.1', '08d71b315819626366b0303f8658fc68')

    depends_on('protobuf', type=('build'))
    depends_on('py-protobuf', type=('build'))
