# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-py6s
#
# You can edit this file again by typing:
#
#     spack edit py-py6s
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------


from spack import *


class PyPy6s(PythonPackage):
    """Py6S is a Python interface to the 6S Radiative Transfer Model. It allows 
       you to run many 6S simulations using a simple Python syntax, rather than 
       dealing with the rather cryptic 6S input and output files."""

    homepage = "http://py6s.rtwilson.com"
    url      = "https://files.pythonhosted.org/packages/5f/7e/c795a9c75436ae50b537d02f70793c6a6129d7f7f8e3f50e9163063d2501/Py6S-1.7.2.tar.gz"

    version('1.7.2', '5c0d0b47607c4ecdf22a81242af8369fc3b99249da0e23e25e9e7ac554d9adcc')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pysolar', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('sixs', type=('build', 'run'))

