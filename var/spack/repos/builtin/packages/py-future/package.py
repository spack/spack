# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFuture(PythonPackage):
    """Clean single-source support for Python 3 and 2"""

    homepage = "https://python-future.org/"
    url = "https://pypi.io/packages/source/f/future/future-0.16.0.tar.gz"

    version('0.16.0', '3e8e88a2bda48d54b1da7634d04760d7')
    version('0.15.2', 'a68eb3c90b3b76714c5ceb8c09ea3a06')

    depends_on('py-setuptools', type='build')
    # depends_on('py-importlib', type=('build', 'run'), when='^python@2.6')
    # depends_on('py-argparse', type=('build', 'run'), when='^python@2.6')
