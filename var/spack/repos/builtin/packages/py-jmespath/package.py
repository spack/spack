# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJmespath(PythonPackage):
    """JMESPath (pronounced "james path") allows you to declaratively
       specify how to extract elements from a JSON document"""

    homepage = "https://github.com/boto/jmespath"
    url      = "https://pypi.io/packages/source/j/jmespath/jmespath-0.9.3.tar.gz"

    version('0.9.3', sha256='6a81d4c9aa62caf061cb517b4d9ad1dd300374cd4706997aff9cd6aedd61fc64')

    depends_on('py-setuptools', type='build')
