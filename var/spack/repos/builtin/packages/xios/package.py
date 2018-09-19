##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
#
from spack import *
import os


class Xios(Package):
    """XML-IO-SERVER library for IO management of climate models."""

    homepage = "https://forge.ipsl.jussieu.fr/ioserver/wiki"

    version('1.0', revision=910,
            svn='http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/branchs/xios-1.0')
    version('develop', svn='http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk')

    variant('mode', values=('debug', 'dev', 'prod'), default='dev',
            description='Build for debugging, development or production')
    # NOTE: oasis coupler could be supported with a variant

    # Use spack versions of blitz and netcdf for compatibility
    # with recent compilers and optimised platform libraries:
    patch('bld_extern_1.0.patch', when='@:1.0')
    patch('bld_extern_1.x.patch', when='@1.1:')

    # Workaround bug #17782 in llvm, where reading a double
    # followed by a character is broken (e.g. duration '1d'):
    patch('llvm_bug_17782.patch', when='@1.1: %clang')

    depends_on('netcdf+mpi')
    depends_on('netcdf-fortran')
    depends_on('hdf5+mpi')
    depends_on('mpi')
    depends_on('boost')
    depends_on('blitz')
    depends_on('perl', type='build')
    depends_on('perl-uri-escape', type='build')
    depends_on('gmake', type='build')

    @when('%clang')
    def patch(self):
        """Fix type references that are ambiguous for clang."""
        for dirpath, dirnames, filenames in os.walk('src'):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                # Use boost definition of type shared_ptr:
                filter_file(r'([^:/])shared_ptr<',
                            r'\1boost::shared_ptr<', filepath)
                # Use type long for position in output stream:
                filter_file(r'oss.tellp\(\) *- *startPos',
                            r'(long)oss.tellp() - startPos', filepath)

    def xios_env(self):
        file = join_path('arch', 'arch-SPACK.env')
        touch(file)

    def xios_path(self):
        file = join_path('arch', 'arch-SPACK.path')
        spec = self.spec
        paths = {'NETCDF_INC_DIR': spec['netcdf'].prefix.include,
                 'NETCDF_LIB_DIR': spec['netcdf'].prefix.lib,
                 'HDF5_INC_DIR': spec['hdf5'].prefix.include,
                 'HDF5_LIB_DIR': spec['hdf5'].prefix.lib}
        text = r"""
NETCDF_INCDIR="-I {NETCDF_INC_DIR}"
NETCDF_LIBDIR="-L {NETCDF_LIB_DIR}"
NETCDF_LIB="-lnetcdff -lnetcdf"

MPI_INCDIR=""
MPI_LIBDIR=""
MPI_LIB=""

HDF5_INCDIR="-I {HDF5_INC_DIR}"
HDF5_LIBDIR="-L {HDF5_LIB_DIR}"
HDF5_LIB="-lhdf5_hl -lhdf5"

OASIS_INCDIR=""
OASIS_LIBDIR=""
OASIS_LIB=""
"""
        with open(file, 'w') as f:
            f.write(text.format(**paths))

    def xios_fcm(self):
        file = join_path('arch', 'arch-SPACK.fcm')
        spec = self.spec
        param = dict()
        param['MPICXX'] = spec['mpi'].mpicxx
        param['MPIFC'] = spec['mpi'].mpifc
        param['CC'] = self.compiler.cc
        param['FC'] = self.compiler.fc
        param['BOOST_INC_DIR'] = spec['boost'].prefix.include
        param['BOOST_LIB_DIR'] = spec['boost'].prefix.lib
        param['BLITZ_INC_DIR'] = spec['blitz'].prefix.include
        param['BLITZ_LIB_DIR'] = spec['blitz'].prefix.lib
        if spec.satisfies('%clang platform=darwin'):
            param['LIBCXX'] = '-lc++'
        else:
            param['LIBCXX'] = '-lstdc++'

        if any(map(spec.satisfies, ('%gcc', '%intel', '%clang'))):
            text = r"""
%CCOMPILER      {MPICXX}
%FCOMPILER      {MPIFC}
%LINKER         {MPIFC}

%BASE_CFLAGS    -ansi -w -D_GLIBCXX_USE_CXX11_ABI=0 \
                -I{BOOST_INC_DIR} -I{BLITZ_INC_DIR}
%PROD_CFLAGS    -O3 -DBOOST_DISABLE_ASSERTS
%DEV_CFLAGS     -g -O2
%DEBUG_CFLAGS   -g

%BASE_FFLAGS    -D__NONE__
%PROD_FFLAGS    -O3
%DEV_FFLAGS     -g -O2
%DEBUG_FFLAGS   -g

%BASE_INC       -D__NONE__
%BASE_LD        -L{BOOST_LIB_DIR} -L{BLITZ_LIB_DIR} -lblitz {LIBCXX}

%CPP            {CC} -E
%FPP            {CC} -E -P -x c
%MAKE           gmake
""".format(**param)
        elif spec.satisfies('%cce'):
            # In the CC compiler prior to cce/8.3.7,
            # optimisation must be reduced to avoid a bug,
            # as reported by Mike Rezny at the UK Met Office:
            if spec.satisfies('%cce@8.3.7:'):
                param.update({'CC_OPT_DEV': '-O2', 'CC_OPT_PROD': '-O3'})
            else:
                param.update({'CC_OPT_DEV': '-O1', 'CC_OPT_PROD': '-O1'})

            text = r"""
%CCOMPILER      {MPICXX}
%FCOMPILER      {MPIFC}
%LINKER         {MPIFC}

%BASE_CFLAGS    -DMPICH_SKIP_MPICXX -h msglevel_4 -h zero -h gnu \
                -I{BOOST_INC_DIR} -I{BLITZ_INC_DIR}
%PROD_CFLAGS    {CC_OPT_PROD} -DBOOST_DISABLE_ASSERTS
%DEV_CFLAGS     {CC_OPT_DEV}
%DEBUG_CFLAGS   -g

%BASE_FFLAGS    -em -m 4 -e0 -eZ
%PROD_FFLAGS    -O3
%DEV_FFLAGS     -G2
%DEBUG_FFLAGS   -g

%BASE_INC       -D__NONE__
%BASE_LD        -D__NONE__ -L{BOOST_LIB_DIR} -L{BLITZ_LIB_DIR} -lblitz

%CPP            cpp
%FPP            cpp -P -CC
%MAKE           gmake
""".format(**param)
        else:
            raise InstallError('Unsupported compiler.')

        with open(file, 'w') as f:
            f.write(text)

    def install(self, spec, prefix):
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc

        options = ['--full',
                   '--%s' % spec.variants['mode'].value,
                   '--arch', 'SPACK',
                   '--netcdf_lib', 'netcdf4_par',
                   '--job', str(make_jobs)]

        self.xios_env()
        self.xios_path()
        self.xios_fcm()

        make_xios = Executable('./make_xios')
        make_xios(*options)

        mkdirp(spec.prefix)
        install_tree('bin', spec.prefix.bin)
        install_tree('lib', spec.prefix.lib)
        install_tree('inc', spec.prefix.include)
        install_tree('etc', spec.prefix.etc)
        install_tree('cfg', spec.prefix.cfg)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_build(self):
        mpirun = os.getenv('MPIRUN')
        if mpirun is None:
            mpirun = 'mpiexec'
        mpiexec = Executable(mpirun)
        with working_dir('inputs'):
            try:
                mpiexec('-n', '2', join_path('..', 'bin', 'test_client.exe'))
            except Exception:
                raise InstallError(
                    'Test failed; defining MPIRUN variable may help.')
