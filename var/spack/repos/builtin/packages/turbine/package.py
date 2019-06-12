# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Turbine(AutotoolsPackage):
    """Turbine: The Swift/T runtime"""

    homepage = 'http://swift-lang.org/Swift-T'
    url      = 'http://swift-lang.github.io/swift-t-downloads/spack/turbine-0.0.0.tar.gz'
    git      = "https://github.com/swift-lang/swift-t.git"
    configure_directory = 'turbine/code'

    version('develop', branch='master')
    version('1.2.3', 'f2e393c292c4248b4e77a19f8272ae88')
    version('1.2.1', 'c8976b22849aafe02a8fb4259dfed434')
    version('1.1.0', '9a347cf16df02707cb529f96c265a082')

    variant('python', default=False,
            description='Enable calling python')
    variant('r', default=False,
            description='Enable calling R')
    variant('hdf5', default=False,
            description='Enable HDF5 support')
    depends_on('adlbx@:0.8.0', when='@:1.1.0')
    depends_on('adlbx', when='@1.2.1:')
    depends_on('adlbx')
    depends_on('tcl', type=('build', 'run'))
    depends_on('zsh', type=('build', 'run'))
    depends_on('swig', type='build')
    depends_on('python', when='+python')
    depends_on('r', when='+r')
    depends_on('r-rinside', when='+r')
    depends_on('hdf5', when='+hdf5')
    depends_on('mpi')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

        spack_env.set('CC', spec['mpi'].mpicc)
        spack_env.set('CXX', spec['mpi'].mpicxx)
        spack_env.set('CXXLD', spec['mpi'].mpicxx)

    def configure_args(self):
        args = ['--with-c-utils=' + self.spec['exmcutils'].prefix,
                '--with-adlb='    + self.spec['adlbx'].prefix,
                '--with-tcl='     + self.spec['tcl'].prefix,
                '--with-mpi='     + self.spec['mpi'].prefix,
                '--disable-static-pkg']
        if '+hdf5' in self.spec:
            args.append('--with-hdf5=ON')
        else:
            args.append('--with-hdf5=OFF')
        if '+python' in self.spec:
            args.append('--with-python-exe={0}'.format(
                        self.spec['python'].command.path))
        if '+r' in self.spec:
            args.append('--with-r={0}/rlib/R'.format(
                        self.spec['r'].prefix))
        return args
