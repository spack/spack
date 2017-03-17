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
from spack import *
import sys


class Mvapich2(Package):
    """MVAPICH2 is an MPI implementation for Infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"
    url = "http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.2.tar.gz"

    version('2.2', '939b65ebe5b89a5bc822cdab0f31f96e')
    version('2.1', '0095ceecb19bbb7fb262131cb9c2cdd6')
    version('2.0', '9fbb68a4111a8b6338e476dc657388b4')
    version('1.9', '5dc58ed08fd3142c260b70fe297e127c')

    patch('ad_lustre_rwcontig_open_source.patch', when='@1.9')

    provides('mpi@:2.2', when='@1.9')  # MVAPICH2-1.9 supports MPI 2.2
    provides('mpi@:3.0', when='@2.0:')  # MVAPICH2-2.0 supports MPI 3.0

    variant('debug', default=False,
            description='Enable debug info and error messages at run-time')

    ##########
    # TODO : Process managers should be grouped into the same variant,
    # as soon as variant capabilities will be extended See
    # https://groups.google.com/forum/#!topic/spack/F8-f8B4_0so
    SLURM = 'slurm'
    HYDRA = 'hydra'
    GFORKER = 'gforker'
    REMSHELL = 'remshell'
    SLURM_INCOMPATIBLE_PMS = (HYDRA, GFORKER, REMSHELL)
    variant(SLURM, default=False,
            description='Set slurm as the only process manager')
    variant(HYDRA, default=False,
            description='Set hydra as one of the process managers')
    variant(GFORKER, default=False,
            description='Set gforker as one of the process managers')
    variant(REMSHELL, default=False,
            description='Set remshell as one of the process managers')
    ##########

    ##########
    # TODO : Network types should be grouped into the same variant, as
    # soon as variant capabilities will be extended
    PSM = 'psm'
    SOCK = 'sock'
    NEMESISIBTCP = 'nemesisibtcp'
    NEMESISIB = 'nemesisib'
    NEMESIS = 'nemesis'
    MRAIL = 'mrail'
    SUPPORTED_NETWORKS = (PSM, SOCK, NEMESIS, NEMESISIB, NEMESISIBTCP)
    variant(
        PSM, default=False,
        description='Configure for QLogic PSM-CH3')
    variant(
        SOCK, default=False,
        description='Configure for TCP/IP-CH3')
    variant(
        NEMESISIBTCP, default=False,
        description='Configure for both OFA-IB-Nemesis and TCP/IP-Nemesis')
    variant(
        NEMESISIB, default=False,
        description='Configure for OFA-IB-Nemesis')
    variant(
        NEMESIS, default=False,
        description='Configure for TCP/IP-Nemesis')
    variant(
        MRAIL, default=False,
        description='Configure for OFA-IB-CH3')
    ##########

    # FIXME : CUDA support is missing
    depends_on('bison')
    depends_on('libpciaccess', when=(sys.platform != 'darwin'))

    def url_for_version(self, version):
        base_url = "http://mvapich.cse.ohio-state.edu/download"
        if version < Version('2.0'):
            return "%s/mvapich2/mv2/mvapich2-%s.tar.gz" % (base_url, version)
        else:
            return "%s/mvapich/mv2/mvapich2-%s.tar.gz"  % (base_url, version)

    @staticmethod
    def enabled(x):
        """Given a variant name returns the string that means the variant is
        enabled

        :param x: variant name
        :return:
        """
        return '+' + x

    def set_build_type(self, spec, configure_args):
        """Appends to configure_args the flags that depends only on the build
        type (i.e. release or debug)

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        if '+debug' in spec:
            build_type_options = [
                "--disable-fast",
                "--enable-error-checking=runtime",
                "--enable-error-messages=all",
                # Permits debugging with TotalView
                "--enable-g=dbg", "--enable-debuginfo"
            ]
        else:
            build_type_options = ["--enable-fast=all"]

        configure_args.extend(build_type_options)

    def set_process_manager(self, spec, configure_args):
        """Appends to configure_args the flags that will enable the
        appropriate process managers

        :param spec: spec
        :param configure_args: list of current configure arguments
        """
        # Check that slurm variant is not activated together with
        # other pm variants
        has_slurm_incompatible_variants = \
            any(self.enabled(x) in spec
                for x in Mvapich2.SLURM_INCOMPATIBLE_PMS)

        if self.enabled(Mvapich2.SLURM) in spec and \
           has_slurm_incompatible_variants:
            raise RuntimeError(" %s : 'slurm' cannot be activated \
            together with other process managers" % self.name)

        process_manager_options = []
        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if self.enabled(Mvapich2.SLURM) in spec:
            if self.version > Version('2.0'):
                process_manager_options = [
                    "--with-pmi=pmi2",
                    "--with-pm=slurm"
                ]
            else:
                process_manager_options = [
                    "--with-pmi=slurm",
                    "--with-pm=no"
                ]

        elif has_slurm_incompatible_variants:
            pms = []
            # The variant name is equal to the process manager name in
            # the configuration options
            for x in Mvapich2.SLURM_INCOMPATIBLE_PMS:
                if self.enabled(x) in spec:
                    pms.append(x)
            process_manager_options = [
                "--with-pm=%s" % ':'.join(pms)
            ]
        configure_args.extend(process_manager_options)

    def set_network_type(self, spec, configure_args):
        # Check that at most one variant has been activated
        count = 0
        for x in Mvapich2.SUPPORTED_NETWORKS:
            if self.enabled(x) in spec:
                count += 1
        if count > 1:
            raise RuntimeError('network variants are mutually exclusive \
            (only one can be selected at a time)')

        network_options = []
        # From here on I can suppose that only one variant has been selected
        if self.enabled(Mvapich2.PSM) in spec:
            network_options = ["--with-device=ch3:psm"]
        elif self.enabled(Mvapich2.SOCK) in spec:
            network_options = ["--with-device=ch3:sock"]
        elif self.enabled(Mvapich2.NEMESISIBTCP) in spec:
            network_options = ["--with-device=ch3:nemesis:ib,tcp"]
        elif self.enabled(Mvapich2.NEMESISIB) in spec:
            network_options = ["--with-device=ch3:nemesis:ib"]
        elif self.enabled(Mvapich2.NEMESIS) in spec:
            network_options = ["--with-device=ch3:nemesis"]
        elif self.enabled(Mvapich2.MRAIL) in spec:
            network_options = ["--with-device=ch3:mrail", "--with-rdma=gen2"]

        configure_args.extend(network_options)

    def setup_environment(self, spack_env, run_env):
        if self.enabled(Mvapich2.SLURM) in self.spec and \
           self.version > Version('2.0'):
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

    def install(self, spec, prefix):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError('Mvapich2 requires both C and Fortran ',
                               'compilers!')

        # we'll set different configure flags depending on our
        # environment
        configure_args = [
            "--prefix=%s" % prefix,
            "--enable-shared",
            "--enable-romio",
            "--disable-silent-rules",
        ]

        if self.compiler.f77 and self.compiler.fc:
            configure_args.append("--enable-fortran=all")
        elif self.compiler.f77:
            configure_args.append("--enable-fortran=f77")
        elif self.compiler.fc:
            configure_args.append("--enable-fortran=fc")
        else:
            configure_args.append("--enable-fortran=none")

        # Set the type of the build (debug, release)
        self.set_build_type(spec, configure_args)
        # Set the process manager
        self.set_process_manager(spec, configure_args)
        # Determine network type by variant
        self.set_network_type(spec, configure_args)

        configure(*configure_args)
        make()
        make("install")

        self.filter_compilers()

    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX, F77, and FC set
           to Spack's generic cc, c++, f77, and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        bin = self.prefix.bin
        mpicc  = join_path(bin, 'mpicc')
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
