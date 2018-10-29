# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPypar(PythonPackage):
    """Pypar is an efficient but easy-to-use module that allows programs
       written in Python to run in parallel on multiple processors and
       communicate using MPI."""
    homepage = "http://code.google.com/p/pypar/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-2.1.5_108.tgz"

    version('2.1.5_108', '7a1f28327d2a3b679f9455c843d850b8')

    depends_on('mpi')
    depends_on('py-numpy', type=('build', 'run'))

    build_directory = 'source'
