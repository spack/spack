# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class PyJeepney(PythonPackage):
    """Low-level, pure Python DBus protocol wrapper."""

    homepage = "https://gitlab.com/takluyver/jeepney"
    pypi = "jeepney/jeepney-0.4.3.tar.gz"

    version('0.7.1', sha256='fa9e232dfa0c498bd0b8a3a73b8d8a31978304dcef0515adc859d4e096f96f4f')
    version('0.6.0', sha256='7d59b6622675ca9e993a6bd38de845051d315f8b0c72cca3aef733a20b648657')
    version('0.4.3', sha256='3479b861cc2b6407de5188695fa1a8d57e5072d7059322469b62628869b8e36e')

    depends_on('python@3.6:', when='@0.5:', type=('build', 'run'))
    depends_on('python@3.5:', when='@:0.4', type=('build', 'run'))
    depends_on('py-flit-core@2:3', type='build')
