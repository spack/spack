# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRequestsToolbelt(PythonPackage):
    """A toolbelt of useful classes and functions to be used with
    python-requests"""

    homepage = "https://toolbelt.readthedocs.org/"
    url      = "https://github.com/requests/toolbelt/archive/0.9.1.tar.gz"

    version('0.9.1', sha256='c8e68e537e87ae088e3a0eb6d80ed5b7cf5d6df503d0e843e0a5e47283db487b')
    version('0.8.0', sha256='f151c07e88148dc05b6f31cc75dfb7a6770968e4a5c8e6690325eed4e79160a1')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.0.1:2.999', type=('build', 'run'))
