# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJunitXml(PythonPackage):
    """Creates JUnit XML test result documents that can be read by tools
    such as Jenkins"""

    homepage = "https://github.com/kyrus/python-junit-xml"
    url      = "https://pypi.io/packages/source/j/junit-xml/junit-xml-1.7.tar.gz"

    version('1.7', '5e6a96edb8a1592f2832241cfd99983e')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
