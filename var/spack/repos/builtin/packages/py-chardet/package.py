# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyChardet(PythonPackage):
    """Universal encoding detector for Python 2 and 3"""

    homepage = "https://github.com/chardet/chardet"
    url      = "https://pypi.io/packages/source/c/chardet/chardet-2.3.0.tar.gz"

    version('3.0.2', sha256='4f7832e7c583348a9eddd927ee8514b3bf717c061f57b21dbe7697211454d9bb')
    version('2.3.0', '25274d664ccb5130adae08047416e1a8')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
