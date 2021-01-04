# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories."""

    homepage = "http://gitpython.readthedocs.org"
    url      = "https://github.com/gitpython-developers/GitPython/archive/3.1.11.tar.gz"

    version('3.1.11', sha256='09440f8ca92759399497d4e3b19b135633a835b2806fa3fd13d90d618b08f9f9')
    version('3.1.10', sha256='bcfd1ccd38c2a287d98fd326c627b9d92730d0dee69a9ba60749cb28b4c1143a')
    version('3.1.8',  sha256='49d4f859bda7bd6ef9ce72d9a2cddb6a59dd70f34a18ce409670bc655431c517')
    version('3.1.7',  sha256='974ded8ca74441cadc8d5c32123595347a7e43d6fefde439735601e6d3a8716b')
    version('3.1.6',  sha256='00d459b1fd2d4a2106252867701f7303485654bdb115275fa6f788756d18879e')
    version('3.1.5',  sha256='2f7f9716afecc099bebf4d1a5e4a7df96f32c8255254e83642d8acf70f1b82c3')
    version('3.1.4',  sha256='946e9c1daa755b8d4aaaad7f96c3fb4ac99ba36379b4355d6a3a4966ba68ca12')
    version('3.1.3',  sha256='12da19250d1db60a9562780c3ecd8a9713da59ec69a3e207db2af1a0afe87c96')
    version('3.1.2',  sha256='ce862c2c5e569728eae2d2441d358ab99a2492c7418cb3bdba1517c46a625cc1')
    version('3.1.1',  sha256='76f35b8d99f02432632d33c0d64419c65d04377cb68b80bfc1819c421a3c05ca')

    depends_on('python@3.5:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-gitdb@4.0.1:4.999', type=('build', 'run'))
