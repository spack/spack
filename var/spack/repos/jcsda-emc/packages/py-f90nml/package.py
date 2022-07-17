# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyF90nml(PythonPackage):
    """A Python module and command line tool for parsing Fortran namelist files"""

    homepage = "https://github.com/marshallward/f90nml"
    pypi     = "f90nml/f90nml-1.4.2.tar.gz"

    maintainers = ['kgerheiser', 'Hang-Lei-NOAA']

    version('1.4.2', sha256='becacc8bed78efa3873438027f898fdd42f3b447c94cd29ae3033d6ff88ab9bb')

    depends_on('py-setuptools', type='build')
