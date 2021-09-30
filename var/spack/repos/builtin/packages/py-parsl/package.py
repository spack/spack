# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParsl(PythonPackage):
    """
    Simple data dependent workflows in Python
    """

    homepage = "https://github.com/Parsl/parsl"
    url      = "https://github.com/Parsl/parsl/archive/refs/tags/1.1.0.tar.gz"

    maintainers = ['hategan']

    version('1.1.0', sha256='6a623d3550329f028775950d23a2cafcb0f82b199f15940180410604aa5d102c')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
