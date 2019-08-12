# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXmlrunner(PythonPackage):
    """PyUnit-based test runner with JUnit like XML reporting."""

    homepage = "https://github.com/pycontribs/xmlrunner"
    url      = "https://pypi.io/packages/source/x/xmlrunner/xmlrunner-1.7.7.tar.gz"

    version('1.7.7', '7b0b152ed2d278516aedbc0cac22dfb3')

    depends_on('py-setuptools', type='build')
    depends_on('py-unittest2', type=('build', 'run'), when='^python@:2.8')
