##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

    # Newer alpha release
    version('2.3a', '87c3fbf8a755b53806fa9ecb21453445')

    # Prefer the latest stable release
    version('2.2', '939b65ebe5b89a5bc822cdab0f31f96e', preferred=True)
    version('2.1', '0095ceecb19bbb7fb262131cb9c2cdd6')
    version('2.0', '9fbb68a4111a8b6338e476dc657388b4')
    version('1.9', '5dc58ed08fd3142c260b70fe297e127c')

    patch('ad_lustre_rwcontig_open_source.patch', when='@1.9')

    provides('mpi')
    provides('mpi@:2.2', when='@1.9')  # MVAPICH2-1.9 supports MPI 2.2
    provides('mpi@:3.0', when='@2.0:')  # MVAPICH2-2.0 supports MPI 3.0

    variant('debug', default=False,
            description='Enable debug info and error messages at run-time')

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

    # FIXME : CUDA support is missing
    depends_on('bison')
    depends_on('libpciaccess', when=(sys.platform != 'darwin'))

    def url_for_version(self, version):
        base_url = "http://mvapich.cse.ohio-state.edu/download"
        if version < Version('2.0'):
            return "%s/mvapich2/mv2/mvapich2-%s.tar.gz" % (base_url, version)
        else:
            return "%s/mvapich/mv2/mvapich2-%s.tar.gz"  % (base_url, version)

    @property
    def process_manager_options(self):
        spec = self.spec

        other_pms = []
        for x in ('hydra', 'gforker', 'remshell'):
            if 'process_managers={0}'.format(x) in spec:
                other_pms.append(x)
        opts = ['--with-pm=%s' % ':'.join(other_pms)]

        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if 'process_managers=slurm' in spec:
            if self.version > Version('2.0'):
                opts = [
                    '--with-pmi=pmi2',
                    '--with-pm=slurm'
                ]
            else:
                opts = [
                    '--with-pmi=slurm',
                    '--with-pm=no'
                ]

        return opts

    @property
    def network_options(self):
        opts = []
        # From here on I can suppose that only one variant has been selected
        if 'fabrics=psm' in self.spec:
            opts = ["--with-device=ch3:psm"]
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
            opts = ["--with-device=ch3:mrail", "--with-rdma=gen2"]
        return opts

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        if 'process_managers=slurm' in spec and spec.satisfies('@2.0:'):
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
            '-disable-silent-rules',
            '--enable-fortran=all',
            "--enable-threads={0}".format(spec.variants['threads'].value),
            "--with-ch3-rank-bits={0}".format(
                spec.variants['ch3_rank_bits'].value),
        ]

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

        args.extend(self.process_manager_options)
        args.extend(self.network_options)
        return args

    @run_after('install')
    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX, F77, and FC set
           to Spack's generic cc, c++, f77, and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        bin = self.prefix.bin
        mpicc = join_path(bin, 'mpicc')
        mpicxx = join_path(bin, 'mpicxx')
        mpif77 = join_path(bin, 'mpif77')
        mpif90 = join_path(bin, 'mpif90')

        # Substitute Spack compile wrappers for the real
        # underlying compiler
        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
        filter_file(env['CC'], self.compiler.cc, mpicc, **kwargs)
        filter_file(env['CXX'], self.compiler.cxx, mpicxx, **kwargs)
        filter_file(env['F77'], self.compiler.f77, mpif77, **kwargs)
        filter_file(env['FC'], self.compiler.fc, mpif90, **kwargs)

        # Remove this linking flag if present
        # (it turns RPATH into RUNPATH)
        for wrapper in (mpicc, mpicxx, mpif77, mpif90):
            filter_file('-Wl,--enable-new-dtags', '', wrapper, **kwargs)
