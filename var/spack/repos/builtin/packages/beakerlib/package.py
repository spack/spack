# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Beakerlib(MakefilePackage):
    """BeakerLib is a shell-level integration testing library, providing
    convenience functions which simplify writing, running and analysis
    of integration and blackbox tests."""

    homepage = "https://github.com/beakerlib/beakerlib"
    url      = "https://github.com/beakerlib/beakerlib/archive/1.20.tar.gz"

    version('1.25', sha256='6fa1007982763218b34d61b5789e17e526cd8e5a99efa9c8ad4f43061bf6ff33')
    version('1.24', sha256='89cc634002f74528bf066fc23bb7d2b8cea16e825ee093baac242b6410074c98')
    version('1.23', sha256='854192cbbb53a5f18d3ec1925367d3f1d22f03cb1349cafce5b917191e5a23d8')
    version('1.22', sha256='8f77f6988177af937bfb3df21c306db443fc2991e1dd7dc90656902d515a31c9')
    version('1.21', sha256='92b155d8424ae7ec48f77e659eee6e5a6921259c610645d757c8ba7e959e3d73')
    version('1.20',   sha256='81f39a0b67adff4c3f4c051ffd26bcf45e19068dee7e81e3b00ee4698587f4e9')
    version('1.19',   sha256='4dcaddf70a057ea5810c967cf5194d11850c8b5263ca25533e9e381067288460')
    version('1.18.1', sha256='65e6f81f17fd87f9db783d0b7a7216387a337f4692d3d9e1c40ef427d977c3d5')

    def install(self, spec, prefix):
        make('DESTDIR={0}'.format(prefix), 'PKGDOCDIR=', 'install')
