# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribApplehelp(PythonPackage):
    """sphinxcontrib-applehelp is a sphinx extension which outputs Apple
    help books."""

    homepage = "http://sphinx-doc.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-applehelp/sphinxcontrib-applehelp-1.0.1.tar.gz"

    version('1.0.1', sha256='edaa0ab2b2bc74403149cb0209d6775c96de797dfd5b5e2a71981309efab3897')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    def test(self):
        # Requires sphinx, creating a circular dependency
        pass
