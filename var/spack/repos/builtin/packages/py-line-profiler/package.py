# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLineProfiler(PythonPackage):
    """Line-by-line profiler."""

    homepage = "https://github.com/rkern/line_profiler"
    url      = "https://pypi.io/packages/source/l/line_profiler/line_profiler-2.0.tar.gz"

    # unfortunately no new release is available and 2.0 does not
    # yet work with python?3.5?: so we use a current commit
    version('2.new', git='git@github.com:rkern/line_profiler.git', commit='3cdc2fab6793802d31130b1af2705bddebf6f7fd')
    version('2.0', 'fc93c6bcfac3b7cb1912cb28836d7ee6')

    depends_on('python@2.5:')
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython',         type='build')
    depends_on('py-ipython@0.13:',  type=('build', 'run'))
