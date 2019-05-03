# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTox(PythonPackage):
    """Tox aims to automate and standardize testing in Python.
       It is part of a larger vision of easing the packaging,
       testing and release process of Python software"""

    homepage = "https://tox.readthedocs.org/"
    url      = "https://pypi.io/packages/source/t/tox/tox-3.5.3.tar.gz"

    version('3.5.3', sha256='513e32fdf2f9e2d583c2f248f47ba9886428c949f068ac54a0469cac55df5862')
    version('2.9.1', sha256='752f5ec561c6c08c5ecb167d3b20f4f4ffc158c0ab78855701a75f5cef05f4b8')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-pluggy@0.3.0:0.99', type=('build', 'run'))
    depends_on('py-py@1.4.17:', type=('build', 'run'))
    depends_on('py-virtualenv@1.11.2:', type=('build', 'run'))
