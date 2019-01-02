# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAdios(PythonPackage):
    """NumPy bindings of ADIOS1"""

    homepage = "https://www.olcf.ornl.gov/center-projects/adios/"
    url      = "https://github.com/ornladios/ADIOS/archive/v1.12.0.tar.gz"
    git      = "https://github.com/ornladios/ADIOS.git"

    maintainers = ['ax3l']

    version('develop', branch='master')
    version('1.13.0', '68af36b821debbdf4748b20320a990ce')
    version('1.12.0', '84a1c71b6698009224f6f748c5257fc9')
    version('1.11.1', '5639bfc235e50bf17ba9dafb14ea4185')
    version('1.11.0', '5eead5b2ccf962f5e6d5f254d29d5238')
    version('1.10.0', 'eff450a4c0130479417cfd63186957f3')
    version('1.9.0', '310ff02388bbaa2b1c1710ee970b5678')

    variant('mpi', default=True,
            description='Enable MPI support')

    for v in ['1.9.0', '1.10.0', '1.11.0', '1.11.1', '1.12.0', '1.13.0',
              'develop']:
        depends_on('adios@{0} ~mpi'.format(v),
                   when='@{0} ~mpi'.format(v),
                   type=['build', 'link', 'run'])
        depends_on('adios@{0} +mpi'.format(v),
                   when='@{0} +mpi'.format(v),
                   type=['build', 'link', 'run'])

    depends_on('py-numpy', type=['build', 'run'])
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', type=['run'], when='+mpi')
    depends_on('py-cython', type=['build'])

    phases = ['build_clib', 'install']
    build_directory = 'wrappers/numpy'

    def setup_file(self):
        """Returns the name of the setup file to use."""
        if '+mpi' in self.spec:
            return 'setup_mpi.py'
        else:
            return 'setup.py'

    def build_clib(self, spec, prefix):
        # calls: make [MPI=y] python
        args = ''
        if '+mpi' in self.spec:
            args = 'MPI=y '
        args += 'python'
        with working_dir(self.build_directory):
            make(args)
