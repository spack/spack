# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBreathe(PythonPackage):
    """Sphinx Doxygen renderer"""

    homepage = "https://github.com/michaeljones/breathe"
    url      = "https://pypi.org/packages/source/b/breathe/breathe-4.11.1.tar.gz"

    version('develop', git=homepage, branch='master', clean=False)
    version('4.11.1', sha256='9b7a94122039ad61383551a696d9c1fa5c16b423a28dadf113389a481d03fad6')

    depends_on('py-setuptools', type='build')
