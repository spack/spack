# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtseq(PythonPackage):
    """HTSeq is a Python package that provides infrastructure to process
    data from high-throughput sequencing assays."""

    homepage = "http://htseq.readthedocs.io/en/release_0.9.1/overview.html"
    url      = "https://github.com/simon-anders/htseq/archive/release_0.9.1.tar.gz"

    version('0.9.1', '269e7de5d39fc31f609cccd4a4740e61')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('swig', type=('build', 'run'))
