# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMemoryProfiler(PythonPackage):
    """A module for monitoring memory usage of a python program"""

    homepage = "https://github.com/fabianp/memory_profiler"
    url      = "https://pypi.io/packages/source/m/memory_profiler/memory_profiler-0.47.tar.gz"

    version('0.47', sha256='e992f2a341a5332dad1ad4a008eeac7cfe78c7ea4abdf7535a3e7e79093328cb')

    depends_on('py-setuptools', type='build')
    depends_on('py-psutil',        type=('build', 'run'))
