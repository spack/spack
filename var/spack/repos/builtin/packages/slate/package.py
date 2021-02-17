# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Slate(CMakePackage):
    """The Software for Linear Algebra Targeting Exascale (SLATE) project is
    to provide fundamental dense linear algebra capabilities to the US
    Department of Energy and to the high-performance computing (HPC) community
    at large. To this end, SLATE will provide basic dense matrix operations
    (e.g., matrix multiplication, rank-k update, triangular solve), linear
    systems solvers, least square solvers, singular value and eigenvalue
    solvers."""

    homepage = "https://icl.utk.edu/slate/"
    git      = "https://bitbucket.org/icl/slate"
    url      = 'https://bitbucket.org/icl/slate/downloads/slate-2020.10.00.tar.gz'
    maintainers = ['G-Ragghianti', 'mgates3']

    test_requires_compiler = True

    version('master', branch='master')
    version('2020.10.00', sha256='ff58840cdbae2991d100dfbaf3ef2f133fc2f43fc05f207dc5e38a41137882ab')

    variant('cuda',   default=True, description='Build with CUDA support.')
    variant('mpi',    default=True, description='Build with MPI support.')
    variant('openmp', default=True, description='Build with OpenMP support.')
    variant('shared', default=True, description='Build shared library')

    depends_on('cuda', when='+cuda')
    depends_on('mpi', when='+mpi')
    depends_on('blas')
    depends_on('blaspp ~cuda', when='~cuda')
    depends_on('blaspp +cuda', when='+cuda')
    depends_on('lapackpp')
    depends_on('lapackpp@2020.10.02:', when='@2020.10.00')
    depends_on('lapackpp@master', when='@master')
    depends_on('scalapack')

    cpp_17_msg = 'Requires C++17 compiler support'
    conflicts('%gcc@:5', msg=cpp_17_msg)
    conflicts('%xl', msg=cpp_17_msg)
    conflicts('%xl_r', msg=cpp_17_msg)
    conflicts('%intel@19:', msg='Does not currently build with icpc >= 2019')

    def cmake_args(self):
        spec = self.spec
        return [
            '-Dbuild_tests=%s'       % self.run_tests,
            '-Duse_openmp=%s'        % ('+openmp' in spec),
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in spec),
            '-Duse_cuda=%s'          % ('+cuda' in spec),
            '-Duse_mpi=%s'           % ('+mpi' in spec),
            '-DSCALAPACK_LIBRARIES=%s'    % spec['scalapack'].libs.joined(';')
        ]

    make_hdr_file = 'make.inc'

    def test(self):
        test_data_dir = self.test_suite.current_test_data_dir
        test_prog = 'slate04_blas'

        config_args = [
            'slate_dir = {0}'.format(self.prefix),
            'scalapack_libs = {0}'.format(self.spec['scalapack'].libs.ld_flags)
        ]
        # Write configuration options to make.inc file
        make_file_inc = join_path(self.install_test_root, self.make_hdr_file)
        with open(make_file_inc, 'w') as inc:
            for option in config_args:
                inc.write('{0}\n'.format(option))
        reason_msg = 'test: slate smoke test'
        with working_dir(test_data_dir, create=False):
            make('all', parallel=False)
            if '+mpi' in self.spec:
                test_args = ['-n', '4', test_prog]
                mpiexe_list = ['mpirun', 'mpiexec', 'srun']
                for mpiexe in mpiexe_list:
                    if which(mpiexe) is not None:
                        self.run_test(mpiexe, test_args, installed=False,
                                      purpose=reason_msg, skip_missing=False,
                                      work_dir='.')
                        break
            else
                self.run_test(test_prog, [], installed=False,
                              purpose=reason_msg, skip_missing=False,
                              work_dir='.')
            #make('clean')
