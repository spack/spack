# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJenkspy(PythonPackage):
    """Compute Natural Breaks (Jenks algorythm)"""

    homepage = "https://github.com/mthh/jenkspy"
    url = "https://pypi.io/packages/source/j/jenkspy/jenkspy-0.1.5.tar.gz"

    version('0.1.5', sha256='e1d4189b620ce5053aaba65736505023586a7ff83f05d9267d6e78c37a13c2b2', preferred=True)

    depends_on('py-setuptools', type='build')
