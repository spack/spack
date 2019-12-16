# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGf256(PythonPackage):
    """GF256 is an implementation of GF(2**8). This Galois Field allows you
       to perform finite field arithmetic on byte sized integers."""

    homepage = "https://github.com/DasIch/gf256/"
    url      = "https://github.com/DasIch/gf256/archive/0.2.0.tar.gz"

    version('0.2.0', 'd56d7fe37ea66c16c4a05bc9d5da646a')

    depends_on('py-setuptools', type='build')
    depends_on('py-cffi@1.7.0:', type=('build', 'run'))
