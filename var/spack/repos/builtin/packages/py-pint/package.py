# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPint(PythonPackage):
    """Pint is a Python package to define, operate and manipulate physical
    quantities: the product of a numerical value and a unit of measurement.
    It allows arithmetic operations between them and conversions from and
    to different units."""

    homepage = "https://pypi.python.org/pypi/pint"
    url      = "https://pypi.io/packages/source/p/pint/Pint-0.8.1.tar.gz"

    version('0.8.1', sha256='afcf31443a478c32bbac4b00337ee9026a13d0e2ac83d30c79151462513bb0d4')

    depends_on('py-setuptools', type='build')
