# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class PyPrecicebindings(PythonPackage):
    """This package provides python language bindings for the C++ library preCICE. """

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/python-bindings.git'
    url      = 'https://github.com/precice/python-bindings/archive/v2.0.0.1.tar.gz'
    # FIXME: Check whether list of maintainers is complete
    maintainers = ['ajaust', 'BenjaminRueth']
    
    # Always prefer final version of release candidate
    version('develop', branch='develop')
    version('2.1.1.1', preferred=True,sha256='972f574549344b6155a8dd415b6d82512e00fa154ca25ae7e36b68d4d2ed2cf4')
    version('2.1.1.1rc2', sha256='beefd2bfab0e9eca6a8f58168d650611193a567479237db0e18a4ca0783269eb')
    version('2.1.1.1rc1',sha256='2fb4ed1a6c12bb3a093d5eac30740a8d0fc61e86bfadbfa37a12e0794059fee5')
    version('2.1.0.1', preferred=True,sha256='ac5cb7412c6b96b08a04fa86ea38e52d91ea739a3bd1c209baa93a8275e4e01a')
    version('2.1.0.1rc2', sha256='eec44ddc4961becb518bc38085cc514a9807f347a508eb0a1021f5afa63fd01b')
    version('2.1.0.1rc1', sha256='2e53629700e4c8ac448e629d704ac0b6c389d8e44c56c017253b203bb34b016e')
    version('2.0.2.1',sha256='c6fca26332316de041f559aecbf23122a85d6348baa5d3252be4ddcd5e94c09a')
    version('2.0.1.1',sha256='2791e7c7e2b04bc918f09f3dfca2d3371e6f8cbb7e57c82bd674703f4fa00be7')
    version('2.0.0.2', preferred=True, sha256='5f055d809d65ec2e81f4d001812a250f50418de59990b47d6bcb12b88da5f5d7')
    version('2.0.0.2rc2',sha256='bc7acb23d22f4ffb868204638d61b36d4ac30a932a2ee43ed886bf1f3ceeb33c')
    version('2.0.0.2rc1',sha256='fa8791e9a1d684fe596a9b853cc60ce5b60a7e4b7c79837a210525f9586293d0')
    version('2.0.0.1',sha256='96eafdf421ec61ad6fcf0ab1d3cf210831a815272984c470b2aea57d4d0c9e0e')
    

    # Import module as a test
    import_modules = ['precice']

    # FIXME: Check if patch is needed
    # FIXME: Check whether patch applies to all binding versions
    patch('remove-unneeded-dependencies.patch')

    variant('mpi', default=True, description='Enables MPI support')

    depends_on("mpi", when="+mpi")
    depends_on("precice@2.1.1", when="@2.1.1.1:2.1.1.99")
    depends_on("precice@2.1.0", when="@2.1.0.1:2.1.0.99")
    depends_on("precice@2.0.2", when="@2.0.2.1:2.0.2.99")
    depends_on("precice@2.0.1", when="@2.0.1.1:2.0.1.99")
    depends_on("precice@2.0.0", when="@2.0.0.1:2.0.0.99")

    # FIXME: Add version numbers to python packages
    depends_on("python@3:", type=('build', 'run'))
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type=('build'))
    depends_on("py-numpy", type=('build', 'run'))
    depends_on("py-mpi4py", type=('build', 'run'), when="+mpi")
    depends_on("py-cython", type=('build'))

    def build_args(self):
        args = []
        return args 


    def build(self, spec, prefix):

        # FIXME: This might was added to enforce usage of correct MPI wrappers. That might not be needed though.
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc

        self.setup_py('build_ext', \
            "--include-dirs={}".format("{}/include".format(self.spec['precice'].prefix) ), \
            "--library-dirs={}".format("{}/lib".format(self.spec['precice'].prefix) ), *( self.build_args() ) )

    def install(self, spec, prefix):
        self.setup_py('install', '--prefix={0}'.format(prefix))
