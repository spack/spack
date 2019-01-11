# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class PyFparser(PythonPackage):
    """Parser for Fortran 77..2003 code."""

    homepage = "https://github.com/stfc/fparser"
    url      = "https://github.com/stfc/fparser/archive/0.0.5.tar.gz"
    git      = "https://github.com/stfc/fparser.git"

    version('develop', branch='master')
    version('0.0.6', '15553fde76b4685fa8edb0a5472b1b53d308c3b8')
    version('0.0.5', '14630afdb8c8bd025e5504c5ab19d133aa8cf8c7')

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type=('build', 'run'), when='@:0.0.5')
    depends_on('py-nose', type='build')
    depends_on('py-six', type='build', when='@0.0.6:')

    depends_on('py-pytest', type='test')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        # Ensure that pytest.ini exists inside the source tree,
        # otherwise an external pytest.ini can cause havoc:
        touch('pytest.ini')
        with working_dir('src'):
            Executable('py.test')()
