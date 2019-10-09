# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTraitlets(PythonPackage):
    """Traitlets Python config system"""

    homepage = "https://pypi.python.org/pypi/traitlets"
    url      = "https://github.com/ipython/traitlets/archive/4.3.1.tar.gz"

    version('4.3.3', sha256='b686c1aadf6ee5a9ee4c22df23bc5cd5bb7b5cfa18afe092e0a139cc2f05fe2e')
    version('4.3.2', sha256='370f938ad730d52272ef74f96f831cb21138f6168e46fe582fe256c35cc656ce')
    version('4.3.1', '146a4885ea64079f62a33b2049841543')
    version('4.3.0', '17af8d1306a401c42dbc92a080722422')
    version('4.2.2', 'ffc03056dc5c8d1fc5dbd6eac76e1e46')
    version('4.2.1', 'fc7f46a76b99ebc5068f99033d268dcf')
    version('4.2.0', '53553a10d124e264fd2e234d0571b7d0')
    version('4.1.0', 'd5bc75c7bd529afb40afce86c2facc3a')
    version('4.0.0', 'b5b95ea5941fd9619b4704dfd8201568')
    version('4.0',   '14544e25ccf8e920ed1cbf833852481f')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-enum34', when='^python@:3.3', type=('build', 'run'))
