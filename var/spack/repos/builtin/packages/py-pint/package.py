# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
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

    version('0.8.1', 'e1f80f3f8fc4e61f68ad3912db26b3a8')

    depends_on('py-setuptools', type='build')
