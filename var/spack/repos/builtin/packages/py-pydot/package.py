# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydot(PythonPackage):
    """Python interface to Graphviz's Dot language"""

    homepage = "https://github.com/erocarrera/pydot/"
    url      = "https://pypi.io/packages/source/p/pydot/pydot-1.2.3.tar.gz"

    version('1.4.1', '0ee9da6823c2fcad4ea380f65730dec5')
    version('1.2.3', '5b50fd8cf022811d8718562ebc8aefb2')
    version('1.2.2', 'fad67d9798dbb33bb3dca3e6d4c47665')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyparsing@2.1.4:', type=('build', 'run'))
    depends_on('graphviz', type=('build', 'run'))
