# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBlack(PythonPackage):
    """Black is the uncompromising Python code formatter. By using it, you agree to
    cede control over minutiae of hand-formatting. In return, Black gives you
    speed, determinism, and freedom from pycodestyle nagging about formatting.
    """

    homepage = "https://github.com/psf/black"
    url      = "https://pypi.io/packages/source/b/black/black-18.9b0.tar.gz"

    version('19.3b0', sha256='68950ffd4d9169716bcb8719a56c07a2f4485354fec061cdd5910aa07369731c')
    version('18.9b0', sha256='e030a9a28f542debc08acceb273f228ac422798e5215ba2a791a6ddeaaca22a5')

    depends_on('python@3.6.0:')
    # Needs setuptools at runtime so that `import pkg_resources` succeeds
    # See #8843 and #8689 for examples of setuptools added as a runtime dep
    depends_on('py-setuptools', type=('build', 'run'))
    # Translated from black's setup.py:
    # https://github.com/ambv/black/blob/master/setup.py
    depends_on('py-attrs@18.1.0:', type=('build', 'run'))
    depends_on('py-click@6.5:', type=('build', 'run'))
    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-toml@0.9.4:', type=('build', 'run'))
