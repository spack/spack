##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
import sys

from spack import *
from spack.error import SpackError


def _process_manager_validator(values):
    if len(values) > 1 and 'slurm' in values:
        raise SpackError(
            'slurm cannot be activated along with other process managers'
        )


class Mvapich2(AutotoolsPackage):
    """MVAPICH2 is an MPI implementation for Infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"
    url = "http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2.tar.gz"
    list_url = "http://mvapich.cse.ohio-state.edu/downloads/"

    version('2.3rc2', '6fcf22fe2a16023b462ef57614daa357')
    version('2.3rc1', '386d79ae36b2136d203826465ad8b6cc')
    version('2.3a', '87c3fbf8a755b53806fa9ecb21453445')

    # Prefer the latest stable release
    version('2.3', sha256='01d5fb592454ddd9ecc17e91c8983b6aea0e7559aa38f410b111c8ef385b50dd', preferred=True)
    version('2.2', '939b65ebe5b89a5bc822cdab0f31f96e')
    version('2.1', '0095ceecb19bbb7fb262131cb9c2cdd6')
    version('2.0', '9fbb68a4111a8b6338e476dc657388b4')

    provides('mpi')
    provides('mpi@:3.0')

    variant('debug', default=False,
            description='Enable debug info and error messages at run-time')

    variant('cuda', default=False,
            description='Enable CUDA extension')

    variant('regcache', default=True,
            description='Enable memory registration cache')

    # Accepted values are:
    #   single      - No threads (MPI_THREAD_SINGLE)
    #   funneled    - Only the main thread calls MPI (MPI_THREAD_FUNNELED)
    #   serialized  - User serializes calls to MPI (MPI_THREAD_SERIALIZED)
    #   multiple    - Fully multi-threaded (MPI_THREAD_MULTIPLE)
    #   runtime     - Alias to "multiple"
    variant(
        'threads',
        default='multiple',
        values=('single', 'funneled', 'serialized', 'multiple'),
        multi=False,
        description='Control the level of thread support'
    )

    # 32 is needed when job size exceeds 32768 cores
    variant(
        'ch3_rank_bits',
        default='32',
        values=('16', '32'),
        multi=False,
        description='Number of bits allocated to the rank field (16 or 32)'
    )

    variant(
        'process_managers',
        description='List of the process managers to activate',
        values=('slurm', 'hydra', 'gforker', 'remshell'),
        multi=True,
        validator=_process_manager_validator
    )

    variant(
        'fabrics',
        description='The fabric enabled for this build',
        default='psm',
        values=(
            'psm', 'sock', 'nemesisib', 'nemesis', 'mrail', 'nemesisibtcp',
            'nemesistcpib'
        )
    )

    variant(
        'alloca',
        default=False,
        description='Use alloca to allocate temporary memory if available'
    )

    variant(
        'file_systems',
        description='List of the ROMIO file systems to activate',
        values=('lustre', 'gpfs', 'nfs', 'ufs'),
        multi=True
    )

    depends_on('bison', type='build')
    depends_on('libpciaccess', when=(sys.platform != 'darwin'))
    depends_on('cuda', when='+cuda')
    depends_on('psm', when='fabrics=psm')
    depends_on('rdma-core', when='fabrics=mrail')
    depends_on('rdma-core', when='fabrics=nemesisib')
    depends_on('rdma-core', when='fabrics=nemesistcpib')
    depends_on('rdma-core', when='fabrics=nemesisibtcp')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpifort', relative_root='bin'
    )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    @property
    def process_manager_options(self):
        spec = self.spec

        other_pms = []
        for x in ('hydra', 'gforker', 'remshell'):
            if 'process_managers={0}'.format(x) in spec:
                other_pms.append(x)

        opts = []
        if len(other_pms) > 0:
            opts = ['--with-pm=%s' % ':'.join(other_pms)]

        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if 'process_managers=slurm' in spec:
            opts = [
                '--with-pmi=pmi2',
                '--with-pm=slurm'
            ]

        return opts

    @property
    def network_options(self):
        opts = []
        # From here on I can suppose that only one variant has been selected
        if 'fabrics=psm' in self.spec:
            opts = [
                "--with-device=ch3:psm",
                "--with-psm={0}".format(self.spec['psm'].prefix)
            ]
        elif 'fabrics=sock' in self.spec:
            opts = ["--with-device=ch3:sock"]
        elif 'fabrics=nemesistcpib' in self.spec:
            opts = ["--with-device=ch3:nemesis:tcp,ib"]
        elif 'fabrics=nemesisibtcp' in self.spec:
            opts = ["--with-device=ch3:nemesis:ib,tcp"]
        elif 'fabrics=nemesisib' in self.spec:
            opts = ["--with-device=ch3:nemesis:ib"]
        elif 'fabrics=nemesis' in self.spec:
            opts = ["--with-device=ch3:nemesis"]
        elif 'fabrics=mrail' in self.spec:
            opts = ["--with-device=ch3:mrail", "--with-rdma=gen2",
                    "--disable-mcast"]
        return opts

    @property
    def file_system_options(self):
        spec = self.spec

        fs = []
        for x in ('lustre', 'gpfs', 'nfs', 'ufs'):
            if 'file_systems={0}'.format(x) in spec:
                fs.append(x)

        opts = []
        if len(fs) > 0:
            opts.append('--with-file-system=%s' % '+'.join(fs))

        return opts

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        # mvapich2 configure fails when F90 and F90FLAGS are set
        spack_env.unset('F90')
        spack_env.unset('F90FLAGS')
        if 'process_managers=slurm' in spec:
            run_env.set('SLURM_MPI_TYPE', 'pmi2')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('MPICH_CC', spack_cc)
        spack_env.set('MPICH_CXX', spack_cxx)
        spack_env.set('MPICH_F77', spack_f77)
        spack_env.set('MPICH_F90', spack_fc)
        spack_env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc  = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpifc  = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpicxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    @run_before('configure')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'Mvapich2 requires both C and Fortran compilers!'
            )

    def configure_args(self):
        spec = self.spec
        args = [
            '--enable-shared',
            '--enable-romio',
            '--disable-silent-rules',
            '--disable-new-dtags',
            '--enable-fortran=all',
            "--enable-threads={0}".format(spec.variants['threads'].value),
            "--with-ch3-rank-bits={0}".format(
                spec.variants['ch3_rank_bits'].value),
        ]

        args.extend(self.enable_or_disable('alloca'))

        if '+debug' in self.spec:
            args.extend([
                '--disable-fast',
                '--enable-error-checking=runtime',
                '--enable-error-messages=all',
                # Permits debugging with TotalView
                '--enable-g=dbg',
                '--enable-debuginfo'
            ])
        else:
            args.append('--enable-fast=all')

        if '+cuda' in self.spec:
            args.extend([
                '--enable-cuda',
                '--with-cuda={0}'.format(spec['cuda'].prefix)
            ])
        else:
            args.append('--disable-cuda')

        if '+regcache' in self.spec:
            args.append('--enable-registration-cache')
        else:
            args.append('--disable-registration-cache')

        args.extend(self.process_manager_options)
        args.extend(self.network_options)
        args.extend(self.file_system_options)
        return args
