# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package_defs import *


class PyAdios(PythonPackage):
    """NumPy bindings of ADIOS1"""

    homepage = "https://csmd.ornl.gov/adios"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.13.1.tar.gz"
    git      = "https://github.com/ornladios/ADIOS.git"

    maintainers = ['ax3l', 'jychoi-hpc']

    version('develop', branch='master')
    version('1.13.1', sha256='b1c6949918f5e69f701cabfe5987c0b286793f1057d4690f04747852544e157b')
    version('1.13.0', sha256='7b5ee8ff7a5f7215f157c484b20adb277ec0250f87510513edcc25d2c4739f50',
            deprecated=True)
    version('1.12.0', sha256='22bc22c157322abec2d1a0817a259efd9057f88c2113e67d918a9a5ebcb3d88d',
            deprecated=True)
    version('1.11.1', sha256='9f5c10b9471a721ba57d1cf6e5a55a7ad139a6c12da87b4dc128539e9eef370e',
            deprecated=True)
    version('1.11.0', sha256='e89d14ccbe7181777225e0ba6c272c0941539b8ccd440e72ed5a9457441dae83',
            deprecated=True)
    version('1.10.0', sha256='6713069259ee7bfd4d03f47640bf841874e9114bab24e7b0c58e310c42a0ec48',
            deprecated=True)
    version('1.9.0', sha256='23b2bb70540d51ab0855af0b205ca484fd1bd963c39580c29e3133f9e6fffd46',
            deprecated=True)

    variant('mpi', default=True,
            description='Enable MPI support')

    for v in ['1.9.0', '1.10.0', '1.11.0', '1.11.1', '1.12.0', '1.13.0', '1.13.1',
              'develop']:
        depends_on('adios@{0} ~mpi'.format(v),
                   when='@{0} ~mpi'.format(v),
                   type=['build', 'link', 'run'])
        depends_on('adios@{0} +mpi'.format(v),
                   when='@{0} +mpi'.format(v),
                   type=['build', 'link', 'run'])

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=['build', 'run'])
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', type=['run'], when='+mpi')
    depends_on('py-cython', type=['build'])

    build_directory = 'wrappers/numpy'

    def patch(self):
        if '+mpi' in self.spec:
            with working_dir(self.build_directory):
                copy('setup_mpi.py', 'setup.py')

    @run_before('install')
    def build_clib(self):
        # calls: make CYTHON=y [MPI=y] python
        args = ['CYTHON=y']
        if '+mpi' in self.spec:
            args += ['MPI=y']
        args += ['python']
        with working_dir(self.build_directory):
            os.remove('adios.cpp')
            os.remove('adios_mpi.cpp')
            make(*args, parallel=False)
