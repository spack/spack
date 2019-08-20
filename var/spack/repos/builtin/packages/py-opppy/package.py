# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpppy(PythonPackage):
    """The Output Parse-Plot Python (OPPPY) library is a python based data
    analysis library designed to extract, store, and plot information from
    output and dump files generated by scientific software packages."""

    homepage = "https://github.com/lanl/opppy"
    url = "https://github.com/lanl/OPPPY/archive/OPPPY-0_1_1.tar.gz"
    git = "https://github.com/lanl/opppy.git"

    version('master', branch='master')
    version('0.1.1', '852a1329ce68d678623beed3fd01ea98')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('python@3:',     type=('build', 'run'))
    depends_on('py-argparse',   type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-sphinx',     type=('build', 'run'))
