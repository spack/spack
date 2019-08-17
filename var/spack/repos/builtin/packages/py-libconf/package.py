# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLibconf(PythonPackage):
    """A pure-Python libconfig reader/writer with permissive license"""

    homepage = "https://pypi.python.org/pypi/libconf"
    url      = "https://pypi.io/packages/source/l/libconf/libconf-1.0.1.tar.gz"

    version('1.0.1', 'd37d355b3248f99802c46669ba38e406')

    depends_on('py-setuptools', type='build')
