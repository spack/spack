# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alps(CMakePackage):
    """Algorithms for Physics Simulations

    Tags: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://alps.comp-phys.org"
    url      = "http://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"

    version('2.3.0', sha256='e64208d1e5acdd6f569277413c4867e1fa366cf4a224570eacbf1e9939fca2d2')

    # Refs for building from source and recipes
    # http://alps.comp-phys.org/mediawiki/index.php/Building_ALPS_from_source
    # https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs/a/ALPS
    # https://github.com/conda-forge/alps-feedstock/tree/master/recipe

    # Package failed to build with boost version >= 1.64
    depends_on('boost@:1.63.0 +chrono +date_time +filesystem +iostreams +mpi +numpy +program_options +python +regex +serialization +system +test +thread +timer')
    depends_on('fftw')
    depends_on('hdf5 ~mpi+hl')
    depends_on('lapack')
    # build fails for latest python@3.7
    depends_on('python@:3.6.99', type=('build', 'link', 'run'))
    depends_on('py-numpy@:1.19.9', type=('build', 'run'))
    depends_on('py-scipy@:1.5.9', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    # fix for gcc@7:
    patch('alps_newgcc.patch', when='%gcc@7:')

    # remove a problematic build variable
    patch('mpi.patch')

    # include climits to use INT_MAX
    patch('alps_climit.patch')

    # ctest tries to test '/usr/bin/time'
    patch('alps_cmake_time.patch')

    extends('python')

    root_cmakelists_dir = 'alps'

    def cmake_args(self):
        args = []
        args.append('Boost_ROOT_DIR=' + self.spec['boost'].prefix)
        args.append("-DCMAKE_CXX_FLAGS={0}".format(self.compiler.cxx98_flag))
        return args

    def test(self):
        troot = self.prefix.tutorials
        test_dir = self.test_suite.current_test_data_dir
        expected = ['Finished with everything.']

        target = 'mc-02-susceptibilities'
        copy_tree(join_path(troot, target), target)
        self.run_test('parameter2xml',
                      options=['parm2a', 'SEED=123456'],
                      work_dir=target
                      )
        self.run_test('spinmc',
                      options=['--Tmin', '10', '--write-xml', 'parm2a.in.xml'],
                      expected=expected, work_dir=target
                      )

        target = 'ed-01-sparsediag'
        copy_tree(join_path(troot, target), target)
        self.run_test('parameter2xml',
                      options=['parm1a', 'SEED=123456'],
                      work_dir=target
                      )
        self.run_test('sparsediag',
                      options=['--write-xml', 'parm1a.in.xml'],
                      expected=expected, work_dir=target
                      )

        target = 'dmrg-01-dmrg'
        copy_tree(join_path(troot, target), target)
        copy(join_path(test_dir, 'spin_one_half'), target)
        self.run_test('parameter2xml',
                      options=['spin_one_half', 'SEED=123456'],
                      work_dir=target
                      )
        self.run_test('dmrg',
                      options=['--write-xml', 'spin_one_half.in.xml'],
                      expected=expected, work_dir=target
                      )
