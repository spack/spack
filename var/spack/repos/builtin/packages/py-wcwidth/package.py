# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWcwidth(PythonPackage):
    """Measures number of Terminal column cells of wide-character codes"""

    pypi = "wcwidth/wcwidth-0.1.7.tar.gz"

    version('0.2.5', sha256='c4d647b99872929fdb7bdcaa4fbe7f01413ed3d98077df798530e5b04f116c83')
    version('0.2.4', sha256='8c6b5b6ee1360b842645f336d9e5d68c55817c26d3050f46b235ef2bc650e48f')
    version('0.2.3', sha256='edbc2b718b4db6cdf393eefe3a420183947d6aa312505ce6754516f458ff8830')
    version('0.2.2', sha256='3de2e41158cb650b91f9654cbf9a3e053cee0719c9df4ddc11e4b568669e9829')
    version('0.2.1', sha256='84e1a7efdafaa87fa6c62aec147a326027e3faa690bff12f10bd9595d6632148')
    version('0.2.0', sha256='70a7fd340fc54ad104b667c7f3c69cfdb52de0a9d2ad7dda94b93588efefb129')
    version('0.1.9', sha256='ee73862862a156bf77ff92b09034fc4825dd3af9cf81bc5b360668d425f3c5f1')
    version('0.1.8', sha256='f28b3e8a6483e5d49e7f8949ac1a78314e740333ae305b4ba5defd3e74fb37a8')
    version('0.1.7', sha256='3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e')

    depends_on('py-setuptools', type='build')
