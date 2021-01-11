# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMemprof(PythonPackage):
    """memprof logs and plots the memory usage of all the
    variables during the execution of the decorated methods."""

    homepage = "http://jmdana.github.io/memprof/"
    url      = "https://github.com/jmdana/memprof/archive/v0.3.6.tar.gz"

    version('0.3.6', sha256='6d94727423224b3ccdde26164ed7ead78d9fbefbfa41c0a30e919c8f6ebc0910')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython',     type='build')
    depends_on('py-argparse',   type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
