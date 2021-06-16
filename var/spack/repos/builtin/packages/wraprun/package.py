# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Wraprun(CMakePackage):
    """wraprun is a utility that enables independent execution of
    multiple MPI applications under a single aprun call."""

    homepage = "https://github.com/olcf/wraprun"
    url      = "https://github.com/olcf/wraprun/archive/refs/tags/v0.2.5.tar.gz"

    version('0.2.5', sha256='19125ab390ff1240651a4294298dee351bb9b236b58a1750aa02bed6d358ee13')

    depends_on('cmake@3.1:', type='build')
    depends_on('mpi')
