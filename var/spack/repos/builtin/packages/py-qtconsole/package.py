# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "http://ipython.org"
    url      = "https://pypi.io/packages/source/q/qtconsole/qtconsole-4.2.1.tar.gz"

    version('4.2.1', 'c08ebebc7a60629ebadf685361ca0798')

    variant('doc', default=False, description='Build documentation')

    depends_on('py-ipykernel@4.1:',      type=('build', 'run'))
    depends_on('py-jupyter-client@4.1:', type=('build', 'run'))
    depends_on('py-jupyter-core',        type=('build', 'run'))
    depends_on('py-pygments',            type=('build', 'run'))
    depends_on('py-traitlets',           type=('build', 'run'))
    depends_on('py-sphinx@1.3:',         type=('build', 'run'), when='+docs')

    depends_on('py-mock', type='test', when='^python@2.7:2.8')
