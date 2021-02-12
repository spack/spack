# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nanopb(CMakePackage):
    """Nanopb is a small code-size Protocol Buffers implementation
    in ansi C."""

    homepage = "https://jpa.kapsi.fi/nanopb/"
    url      = "https://github.com/nanopb/nanopb/archive/0.3.9.1.tar.gz"

    version('0.4.4',   sha256='66621e896c1e357d21b4e5bcc87584afd95abe18ea7a3314ce2696048ab340db')
    version('0.4.3',   sha256='cc3beaff146ffa0111ff92e5feac5791e6a49c5307dde4d3aae68424a53b0d3b')
    version('0.4.2',   sha256='c132c845f9a407370c180a47db5bc683817024dbf67aee57e51fd0586b02556e')
    version('0.3.9.7', sha256='12b9d1318003f9b331b592165ad436d92c5bcf4193c7986fc6d41d2710f0d6a6')
    version('0.3.9.6', sha256='a2392711f28f24725cea791ebeea172d91474e769667c1d5061ef6cf086fa3aa')
    version('0.3.9.1', sha256='b22d1f86d4adb2aa0436a277c4a59a5adfc467cafeb9bf405c27ef136599bbb3')

    depends_on('protobuf', type=('build'))
    depends_on('py-protobuf', type=('build'))
