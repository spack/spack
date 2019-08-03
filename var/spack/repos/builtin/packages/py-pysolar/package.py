# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-pysolar
#
# You can edit this file again by typing:
#
#     spack edit py-pysolar
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PyPysolar(PythonPackage):
    """Pysolar is a collection of Python libraries for simulating the 
       irradiation of any point on earth by the sun. It includes code 
       for extremely precise ephemeris calculations, and more."""

    homepage = "http://pysolar.readthedocs.io"
    url      = "https://github.com/pingswept/pysolar/archive/0.6.tar.gz"

    version('0.6',       '78005c1e498100cc30842af20ca76069')

    depends_on('py-setuptools', type='build')

