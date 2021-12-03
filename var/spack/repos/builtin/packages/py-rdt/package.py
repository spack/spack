# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRdt(PythonPackage):
    """RDT is a Python library used to transform data for data science libraries and preserve the transformations in order to revert them as needed."""

    homepage = "https://github.com/sdv-dev/RDT"
    pypi     = "rdt/rdt-0.6.1.tar.gz"

    version('0.6.1', sha256='ee2ac0d3479b254f99f35a709a24ffd5f2c899de6ea71f1ee844c6113febba71')
    version('0.6.0', sha256='db83f7f3f4f79bfc38a9fcb8b9b45fdfa1bb7a5e840239d9c4372572945ac3d6')
    version('0.5.3', sha256='6156e8935ff3b7e0489c789ba2bd7e83e7ef7963c6fc03565e91dc52e6c91d52')

    depends_on('python@3.6:',                           type=('build', 'run'))
    depends_on('py-setuptools',                         type='build')
    depends_on('py-numpy@1.18.0:1.19.999',              type=('build', 'run'), when= '+ python@3.6')
    depends_on('py-numpy@1.20:',                        type=('build', 'run'), when= '+ python@3.7:')
    depends_on('py-pandas@1.1.3:1.999.999',             type=('build', 'run'), when= '@0.6.1')
    depends_on('py-pandas@1.1.0:1.1.4',                 type=('build', 'run'), when= '@0.5.3:0.6.0')
    depends_on('py-scipy@1.5.4:1.999.999',              type=('build', 'run'), when= '@0.6.1')
    depends_on('py-scipy@1.4.1:1.999.999',              type=('build', 'run'), when= '@0.5.3:0.6.0')
    depends_on('py-psutil@5.7:5.999',                   type=('build', 'run'))
