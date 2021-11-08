# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyAbslPy(PythonPackage):
    """
    This repository is a collection of Python library code for building
    Python applications.

    The code is collected from Google's own Python code base, and has been
    extensively tested and used in production.
    """

    pypi = "absl-py/absl-py-0.7.0.tar.gz"

    version('0.13.0', sha256='6953272383486044699fd0e9f00aad167a27e08ce19aae66c6c4b10e7e767793')
    version('0.12.0', sha256='b44f68984a5ceb2607d135a615999b93924c771238a63920d17d3387b0d229d5')
    version('0.11.0', sha256='673cccb88d810e5627d0c1c818158485d106f65a583880e2f730c997399bcfa7')
    version('0.10.0', sha256='b20f504a7871a580be5268a18fbad48af4203df5d33dbc9272426cb806245a45')
    version('0.7.1', sha256='b943d1c567743ed0455878fcd60bc28ac9fae38d129d1ccfad58079da00b8951')
    version('0.7.0', sha256='8718189e4bd6013bf79910b9d1cb0a76aecad8ce664f78e1144980fabdd2cd23')
    version('0.1.6', sha256='02c577d618a8bc0a2a5d1a51f160d3649745d7a2516d87025322f46ac1391a22')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')
