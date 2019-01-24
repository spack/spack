# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAsyncGenerator(PythonPackage):
    """Provides async generator functionality to python 3.5."""

    homepage = "https://pypi.org/project/async_generator/"
    url      = "https://files.pythonhosted.org/packages/ce/b6/6fa6b3b598a03cba5e80f829e0dadbb49d7645f523d209b2fb7ea0bbb02a/async_generator-1.10.tar.gz"

    version('1.10', sha256='6ebb3d106c12920aaae42ccb6f787ef5eefdcdd166ea3d628fa8476abe712144')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5:')
