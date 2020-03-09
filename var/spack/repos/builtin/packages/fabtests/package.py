# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fabtests(AutotoolsPackage):
    """Fabtests provides a set of examples that uses libfabric.

    DEPRECATED. Fabtests has merged with the libfabric git repo."""

    homepage = "http://libfabric.org"
    url      = "https://github.com/ofiwg/fabtests/releases/download/v1.5.3/fabtests-1.5.3.tar.gz"

    version('1.6.0', sha256='dc3eeccccb005205017f5af60681ede15782ce202a0103450a6d56a7ff515a67')
    version('1.5.3', sha256='3835b3bf86cd00d23df0ddba8bf317e4a195e8d5c3c2baa918b373d548f77f29')

    depends_on('libfabric@1.6.0', when='@1.6.0')
    depends_on('libfabric@1.5.3', when='@1.5.3')
