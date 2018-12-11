# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPynio(PythonPackage):
    """PyNIO ("pie-nee-oh") is a Python module that allows read and/or
       write access to a variety of scientific data formats popular in
       climate and weather"""

    homepage = "https://www.pyngl.ucar.edu/Nio.shtml"
    url      = "https://github.com/NCAR/pynio/archive/1.5.4.tar.gz"

    version('1.5.4', sha256='e5bb57d902740d25e4781a9f89e888149f55f2ffe60f9a5ad71069f017c89e1a')

    depends_on('netcdf')
    depends_on('libpng')
    depends_on('py-numpy', type=('build', 'run'))
