# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cram(CMakePackage):
    """Cram runs many small MPI jobs inside one large MPI job."""
    homepage = "https://github.com/llnl/cram"
    url      = "http://github.com/llnl/cram/archive/v1.0.1.tar.gz"

    version('1.0.1', 'c73711e945cf5dc603e44395f6647f5e')

    extends('python@2.7:')
    depends_on('mpi')
    depends_on('cmake@2.8:', type='build')
