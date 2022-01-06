# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAts(PythonPackage):
    """ATS - Automated Testing System - is an open-source, Python-based tool
    for automating the running of tests of an application across a broad range
    of high performance computers."""

    homepage = "https://github.com/LLNL/ATS"
    git      = "https://github.com/LLNL/ATS.git"

    maintainers = ['white238']

    version('main', branch='main')
    version('7.0.10', tag='7.0.10')
    version('7.0.5.9', tag='7.0.5.9')
    version('7.0.5.8', tag='7.0.5.8')
    version('7.0.5.7', tag='7.0.5.7')
    version('7.0.5.6', tag='7.0.5.6')
    version('7.0.5.5', tag='7.0.5.5')
    version('7.0.5.4', tag='7.0.5.4')
    version('7.0.5.3', tag='7.0.5.3')
    version('7.0.5.2', tag='7.0.5.2')
    version('7.0.5.1', tag='7.0.5.1')
    version('7.0.5', tag='7.0.5')
    version('7.0.4', tag='7.0.4')

    # TODO: Add flux variant when Flux functionality works in ATS

    depends_on("python@3.8:", type=('build', 'run'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on('py-setuptools', type='build')
