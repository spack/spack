# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySimplejson(PythonPackage):
    """Simplejson is a simple, fast, extensible JSON encoder/decoder for
    Python"""

    homepage = "https://github.com/simplejson/simplejson"
    url      = "https://pypi.io/packages/source/s/simplejson/simplejson-3.10.0.tar.gz"

    version('3.10.0', '426a9631d22851a7a970b1a677368b15')
    version('3.9.0',  '01db2db1b96bd8e59bcab45bca12639b')
    version('3.8.2',  '53b1371bbf883b129a12d594a97e9a18')
    version('3.8.1',  'b8441f1053edd9dc335ded8c7f98a974')
    version('3.8.0',  '72f3b93a6f9808df81535f79e79565a2')

    depends_on('py-setuptools', type='build')
