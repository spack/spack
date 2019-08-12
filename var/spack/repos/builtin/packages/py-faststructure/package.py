# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFaststructure(PythonPackage):
    """FastStructure is a fast algorithm for inferring population structure
       from large SNP genotype data."""

    homepage = "https://github.com/rajanil/fastStructure"
    url      = "https://github.com/rajanil/fastStructure/archive/v1.0.tar.gz"

    version('1.0', '5cbb76e7d49e27a57046ab641b666f97')

    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('gsl')
