# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyH5py(PythonPackage):
    """The h5py package provides both a high- and low-level interface to the
    HDF5 library from Python."""

    homepage = "https://www.h5py.org/"
    pypi     = "h5py/h5py-3.3.0.tar.gz"
    git      = "https://github.com/h5py/h5py.git"
    maintainers = ['bryanherman', 'takluyver']

    version('master', branch='master')
    version('3.6.0', sha256='8752d2814a92aba4e2b2a5922d2782d0029102d99caaf3c201a566bc0b40db29')
    version('3.5.0', sha256='77c7be4001ac7d3ed80477de5b6942501d782de1bbe4886597bdfec2a7ab821f')
    version('3.4.0', sha256='ee1c683d91ab010d5e85cb61e8f9e7ee0d8eab545bf3dd50a9618f1d0e8f615e')
    version('3.3.0', sha256='e0dac887d779929778b3cfd13309a939359cc9e74756fc09af7c527a82797186')
    version('3.2.1', sha256='89474be911bfcdb34cbf0d98b8ec48b578c27a89fdb1ae4ee7513f1ef8d9249e')
    version('3.2.0', sha256='4271c1a4b7d87aa76fe96d016368beb05a6c389d64882d58036964ce7d2d03c1')
    version('3.1.0', sha256='1e2516f190652beedcb8c7acfa1c6fa92d99b42331cbef5e5c7ec2d65b0fc3c2')
    version('3.0.0', sha256='7d3803be1b530c68c2955faba726dc0f591079b68941a0c0269b5384a42ab519')
    version('2.10.0', sha256='84412798925dc870ffd7107f045d7659e60f5d46d1c70c700375248bf6bf512d')
    version('2.9.0', sha256='9d41ca62daf36d6b6515ab8765e4c8c4388ee18e2a665701fef2b41563821002')
    version('2.8.0', sha256='e626c65a8587921ebc7fb8d31a49addfdd0b9a9aa96315ea484c09803337b955')
    version('2.7.1', sha256='180a688311e826ff6ae6d3bda9b5c292b90b28787525ddfcb10a29d5ddcae2cc')
    version('2.7.0', sha256='79254312df2e6154c4928f5e3b22f7a2847b6e5ffb05ddc33e37b16e76d36310')
    version('2.6.0', sha256='b2afc35430d5e4c3435c996e4f4ea2aba1ea5610e2d2f46c9cae9f785e33c435')
    version('2.5.0', sha256='9833df8a679e108b561670b245bcf9f3a827b10ccb3a5fa1341523852cfac2f6')
    version('2.4.0', sha256='faaeadf4b8ca14c054b7568842e0d12690de7d5d68af4ecce5d7b8fc104d8e60')

    variant('mpi', default=True, description='Build with MPI support')

    # Python versions
    depends_on('python@3.6:', type=('build', 'run'), when='@3:3.1')
    depends_on('python@3.7:', type=('build', 'run'), when='@3.2:')

    # Build dependencies
    depends_on('py-cython@0.23:', type='build', when='@:2')
    depends_on('py-cython@0.29:', type=('build'), when='@3: ^python@:3.7')
    depends_on('py-cython@0.29.14:', type=('build'), when='@3: ^python@3.8.0:3.8')
    depends_on('py-cython@0.29.15:', type=('build'), when='@3: ^python@3.9.0:')
    depends_on('py-pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build', when='@3:')

    # Build and runtime dependencies
    depends_on('py-cached-property@1.5:', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-numpy@1.7:', type=('build', 'run'), when='@:2')
    depends_on('py-numpy@1.12:', type=('build', 'run'), when='@3: ^python@3.6.0:3.6')
    depends_on('py-numpy@1.14.5:', type=('build', 'run'), when='@3: ^python@3.7.0:3.7')
    depends_on('py-numpy@1.17.5:', type=('build', 'run'), when='@3: ^python@3.8.0:3.8')
    depends_on('py-numpy@1.19.3:', type=('build', 'run'), when='@3: ^python@3.9.0:')
    depends_on('py-six', type=('build', 'run'), when='@:2')

    # Link dependencies (py-h5py v2 cannot build against HDF5 1.12 regardless
    # of API setting)
    depends_on('hdf5@1.8.4:1.11 +hl', when='@:2')
    depends_on('hdf5@1.8.4: +hl', when='@3:')

    # MPI dependencies
    depends_on('hdf5+mpi', when='+mpi')
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='@:2 +mpi', type=('build', 'run'))
    depends_on('py-mpi4py@3:', when='@3:3.2+mpi^python@3:3.7', type=('build', 'run'))
    depends_on('py-mpi4py@3.0.2:', when='@3.3.0:+mpi^python@3:3.7', type=('build', 'run'))
    depends_on('py-mpi4py@3.0.3:', when='@3:+mpi^python@3.8.0:', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('HDF5_DIR', self.spec['hdf5'].prefix)
        if '+mpi' in self.spec:
            env.set('CC', self.spec['mpi'].mpicc)
            env.set('HDF5_MPI', 'ON')

        # Disable build requirements meant for Python build tools, which pin
        # versions of numpy & mpi4py.
        env.set('H5PY_SETUP_REQUIRES', '0')
