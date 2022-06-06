# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DxtExplorer(PythonPackage):
    """DXT Explorer is an interactive web-based log analysis tool to visualize Darshan DXT logs and help understand the I/O behavior of applications."""

    homepage = "http://dxt-explorer.readthedocs.io"
    git      = "https://github.com/hpc-io/dxt-explorer"
    pypi     = "dxt-explorer/dxt-explorer-0.2.tar.gz"

    maintainers = ['jeanbez', 'sbyna']
 
    version('0.2', sha256='410d8657a7a3288233ee39a128582eca089538cfc5232799dd15c582c167f164')
    
    version('develop', branch='develop')
    version('tests', branch='index-file')
    
    depends_on('r', type=('run'))

    depends_on('darshan-util', type=('run'))

    depends_on('py-pip', type='build')
    depends_on('py-pandas', type='run')
    depends_on('py-pytest', type=('build', 'test'))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir('.', create=True):
            pytest = which('pytest')
            pytest()
