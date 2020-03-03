# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sgpp(SConsPackage):
    """Sparse grids library"""

    homepage = "https://sgpp.sparsegrids.org"
    url = "https://github.com/SGpp/SGpp/archive/v3.2.0.tar.gz"
    maintainers = ['G-071', 'leiterrl']

    # Versions with Python 3 bindings:
    version('master', git='https://github.com/SGpp/SGpp.git', branch='master')
    version('3.2.0', sha256='dab83587fd447f92ed8546eacaac6b8cbe65b8db5e860218c0fa2e42f776962d')
    # Versions with Python 2 bindings:
    version('3.1.0', sha256='6b46bc5b3966e92567d6754130666bdffb7be1d1d2c1b427d7ce964b8eaab526')
    version('3.0.0', sha256='4dd9049e664abd7db78c355fea5e192167812f443115d4bf686a51bb1e9bda9c')

    # Patch that ensures libraries will actually
    # be copied into prefix/lib upon installation
    # (otherwise it would be prefix/sgpp/lib)
    patch('directory.patch')
    # Fix faulty setup.py in 3.2.0
    patch('fix-setup-py.patch', when='@3.2.0')
    # Backport opencl fix from master
    patch('ocl.patch', when='@:3.2.0+opencl')

    variant('simd',
            default='avx2',
            values=('sse3', 'sse42', 'avx', 'fma4', 'avx2', 'avx512'),
            description='Specifies the SIMD extension to be used')
    variant('python', default=False,
            description='Provide Python bindings for SGpp')
    variant('java', default=False,
            description='Provide Java bindings for SGpp')
    # export CLASSPATH=$(spack location --install-dir sgpp)/lib/jsgpp.jar
    # After that one can compile and run simple java examples with sgpp
    variant('optimization', default=False,
            description='Builds the optimization module of SGpp')
    variant('pde', default=False,
            description='Builds the datadriven module of SGpp')
    variant('quadrature', default=False,
            description='Builds the datadriven module of SGpp')
    variant('datadriven', default=False,
            description='Builds the datadriven module of SGpp')
    variant('misc', default=False,
            description='Builds the misc module of SGpp')
    variant('combigrid', default=False,
            description='Builds the combigrid module of SGpp')
    variant('solver', default=False,
            description='Builds the solver module of SGpp')
    variant('opencl', default=False,
            description='Enables support for OpenCL accelerated operations')
    variant('mpi', default=False,
            description='Enables support for MPI-distributed operations')

    # Mandatory dependencies
    depends_on('scons@2.5.1', when='@:3.1.0', type=('build'))
    depends_on('scons@3:', when='@3.2.0:', type=('build'))
    depends_on('zlib', type=('build', 'run'))
    # Python dependencies
    extends('python', when='+python')
    # Python 3 support was added in version 3.2.0
    depends_on('python@2.7:2.8', when='@:3.1.0+python', type=('build', 'run'))
    depends_on('python@3:', when='@3.2.0:+python', type=('build', 'run'))
    depends_on('swig@3:', when='+python', type=('build'))
    # Java dependencies
    depends_on('swig@3:', when='+java', type=('build'))
    depends_on('openjdk', when='+java', type=('build', 'run'))
    # Python libraries (version depends on whether we use Python 2 or 3)
    depends_on('py-numpy@:1.16', when='@:3.1.0+python', type=('build', 'run'))
    depends_on('py-numpy@1.17:', when='@3.2.0:+python', type=('build', 'run'))
    depends_on('py-scipy@:1.2.3', when='@:3.1.0+python', type=('build', 'run'))
    depends_on('py-scipy@1.3.0:', when='@3.2.0:+python', type=('build', 'run'))
    # MPI dependency
    depends_on('mpi', when='+mpi', type=('build', 'run'))

    # Solver python bindings are actually using the pde module at one point:
    conflicts('-pde', when='+python+solver')
    # some modules depend on each other (notably datadriven and misc)
    conflicts('+datadriven', when='-optimization')
    conflicts('+datadriven', when='-pde')
    conflicts('+misc', when='-datadriven')
    # Misc did not exist in older versions
    conflicts('+misc', when='@:3.1.0')
    # Datadriven requires at least avx
    conflicts('+datadriven', when='simd=sse3')
    conflicts('+datadriven', when='simd=sse42')

    def build_args(self, spec, prefix):
        # No need for unit tests anymore -> saves installation time
        self.args = ['COMPILE_BOOST_TESTS=0',
                     'RUN_BOOST_TESTS=0',
                     'RUN_PYTHON_TESTS=0']
        # No need to check the code style anymore -> saves installation time
        if any(x in spec for x in ['@3.2.0', '@3.1.0', '@3.0.0']):
            self.args.append('RUN_CPPLINT=0')
        else:  # argument was renamed after 3.2.0
            self.args.append('CHECK_STYLE=0')
        # Install direction
        self.args.append('PREFIX={0}'.format(prefix))
        # Generate swig bindings?
        self.args.append('SG_JAVA={0}'.format(
            '1' if '+java' in spec else '0'))
        self.args.append('SG_PYTHON={0}'.format(
            '1' if '+python' in spec else '0'))
        # Which modules to build?
        self.args.append('SG_OPTIMIZATION={0}'.format(
            '1' if '+optimization' in spec else '0'))
        self.args.append('SG_QUADRATURE={0}'.format(
            '1' if '+quadrature' in spec else '0'))
        self.args.append('SG_PDE={0}'.format(
            '1' if '+pde' in spec else '0'))
        self.args.append('SG_DATADRIVEN={0}'.format(
            '1' if '+datadriven' in spec else '0'))
        self.args.append('SG_COMBIGRID={0}'.format(
            '1' if '+combigrid' in spec else '0'))
        self.args.append('SG_SOLVER={0}'.format(
            '1' if '+solver' in spec else '0'))
        self.args.append('ARCH={0}'.format(
            spec.variants['simd'].value))
        self.args.append('USE_OCL={0}'.format(
            '1' if '+opencl' in spec else '0'))
        # Misc did not exist in older versions
        if all(x not in spec for x in ['@3.1.0', '@3.0.0']):
            self.args.append('SG_MISC={0}'.format(
                '1' if '+misc' in spec else '0'))
        # Get the mpicxx compiler from the Spack spec
        # (makes certain we use the one from spack):
        if ('+mpi' in spec):
            self.args.append('CXX={0}'.format(
                self.spec['mpi'].mpicxx))
        return self.args

    def install_args(self, spec, prefix):
        # Everything is already built, time to install our python bindings:
        if '+python' in spec:
            setup_py('install', '--prefix={0}'.format(prefix))
        return self.args
