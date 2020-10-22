# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVisdom(PythonPackage):
    """Visdom aims to facilitate visualization of (remote) data
    with an emphasis on supporting scientific
    experimentation."""

    homepage = "https://github.com/facebookresearch/visdom"
    url      = "https://files.pythonhosted.org/packages/c9/75/e078f5a2e1df7e0d3044749089fc2823e62d029cc027ed8ae5d71fafcbdc/visdom-0.1.8.9.tar.gz"

    version('0.1.8.9', sha256='c73ad23723c24a48156899f78dd76bd4538eba3edf9120b6c65a9528fa677126')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.8:', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-tornado', type=('build', 'run'))
    depends_on('py-pyzmq', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-jsonpatch', type=('build', 'run'))
    depends_on('py-websocket-client', type=('build', 'run'))
    depends_on('py-torch@0.3.1:', type=('build', 'run'))
    depends_on('py-pillow', type=('build', 'run'))
    depends_on('py-torchfile', type=('build', 'run'))
