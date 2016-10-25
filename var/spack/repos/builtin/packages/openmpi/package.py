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
import os

import llnl.util.tty as tty

from spack import *


def _verbs_dir():
    """
    Try to find the directory where the OpenFabrics verbs package is
    installed. Return None if not found.
    """
    try:
        # Try to locate Verbs by looking for a utility in the path
        ibv_devices = which("ibv_devices")
        # Run it (silently) to ensure it works
        ibv_devices(output=str, error=str)
        # Get path to executable
        path = ibv_devices.exe[0]
        # Remove executable name and "bin" directory
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        # There's usually no "/include" on Unix; use "/usr/include" instead
        if path == "/":
            path = "/usr"
        return path
    except:
        return None


class Openmpi(Package):
    """The Open MPI Project is an open source Message Passing Interface
       implementation that is developed and maintained by a consortium
       of academic, research, and industry partners. Open MPI is
       therefore able to combine the expertise, technologies, and
       resources from all across the High Performance Computing
       community in order to build the best MPI library available.
       Open MPI offers advantages for system and software vendors,
       application developers and computer science researchers.
    """

    homepage = "http://www.open-mpi.org"
    url = "http://www.open-mpi.org/software/ompi/v1.10/downloads/openmpi-1.10.1.tar.bz2"
    list_url = "http://www.open-mpi.org/software/ompi/"
    list_depth = 3

    version('2.0.1', '6f78155bd7203039d2448390f3b51c96')
    version('2.0.0', 'cdacc800cb4ce690c1f1273cb6366674')
    version('1.10.3', 'e2fe4513200e2aaa1500b762342c674b')
    version('1.10.2', 'b2f43d9635d2d52826e5ef9feb97fd4c')
    version('1.10.1', 'f0fcd77ed345b7eafb431968124ba16e')
    version('1.10.0', '280cf952de68369cebaca886c5ce0304')
    version('1.8.8', '0dab8e602372da1425e9242ae37faf8c')
    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475')

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")
    patch('configure.patch', when="@1.10.0:1.10.1")

    variant('psm', default=False, description='Build support for the PSM library.')
    variant('psm2', default=False,
            description='Build support for the Intel PSM2 library.')
    variant('pmi', default=False,
            description='Build support for PMI-based launchers')
    variant('verbs', default=_verbs_dir() is not None,
            description='Build support for OpenFabrics verbs.')
    variant('mxm', default=False, description='Build Mellanox Messaging support')

    variant('thread_multiple', default=False,
            description='Enable MPI_THREAD_MULTIPLE support')

    # TODO : variant support for alps, loadleveler  is missing
    variant('tm', default=False,
            description='Build TM (Torque, PBSPro, and compatible) support')
    variant('slurm', default=False,
            description='Build SLURM scheduler component')

    variant('sqlite3', default=False, description='Build sqlite3 support')

    variant('vt', default=True,
            description='Build support for contributed package vt')

    # TODO : support for CUDA is missing

    provides('mpi@:2.2', when='@1.6.5')
    provides('mpi@:3.0', when='@1.7.5:')
    provides('mpi@:3.1', when='@2.0.0:')

    depends_on('hwloc')
    depends_on('sqlite', when='+sqlite3')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/ompi/v%s/downloads/openmpi-%s.tar.bz2" % (
            version.up_to(2), version)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

    def setup_dependent_package(self, module, dep_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpic++')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpi_cxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def setup_environment(self, spack_env, run_env):
        # As of 06/2016 there is no mechanism to specify that packages which
        # depends on MPI need C or/and Fortran implementation. For now
        # require both.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            tty.warn('OpenMPI : FORTRAN compiler not found')
            tty.warn('OpenMPI : FORTRAN bindings will be disabled')
            spack_env.unset('FC')
            spack_env.unset('F77')
            # Setting an attribute here and using it in the 'install'
            # method is needed to ensure tty.warn is actually displayed
            # to user and not redirected to spack-build.out
            self.config_extra = ['--enable-mpi-fortran=none',
                                 '--disable-oshmem-fortran']

    @property
    def verbs(self):
        # Up through version 1.6, this option was previously named
        # --with-openib
        if self.spec.satisfies('@:1.6'):
            return 'openib'
        # In version 1.7, it was renamed to be --with-verbs
        elif self.spec.satisfies('@1.7:'):
            return 'verbs'

    def install(self, spec, prefix):
        config_args = ["--prefix=%s" % prefix,
                       "--with-hwloc=%s" % spec['hwloc'].prefix,
                       "--enable-shared",
                       "--enable-static"]

        # for Open-MPI 2.0:, C++ bindings are disabled by default.
        if self.spec.satisfies('@2.0:'):
            config_args.extend(['--enable-mpi-cxx'])

        if getattr(self, 'config_extra', None) is not None:
            config_args.extend(self.config_extra)

        # Variant based arguments
        config_args.extend([
            # Schedulers
            '--with-tm' if '+tm' in spec else '--without-tm',
            '--with-slurm' if '+slurm' in spec else '--without-slurm',
            # Fabrics
            '--with-psm' if '+psm' in spec else '--without-psm',
            '--with-psm2' if '+psm2' in spec else '--without-psm2',
            '--with-mxm' if '+mxm' in spec else '--without-mxm',
            # Other options
            ('--enable-mpi-thread-multiple' if '+thread_multiple' in spec
                else '--disable-mpi-thread-multiple'),
            '--with-pmi' if '+pmi' in spec else '--without-pmi',
            '--with-sqlite3' if '+sqlite3' in spec else '--without-sqlite3',
            '--enable-vt' if '+vt' in spec else '--disable-vt'
        ])
        if '+verbs' in spec:
            path = _verbs_dir()
            if path is not None and path not in ('/usr', '/usr/local'):
                config_args.append('--with-%s=%s' % (self.verbs, path))
            else:
                config_args.append('--with-%s' % self.verbs)
        else:
            config_args.append('--without-%s' % self.verbs)

        # TODO: use variants for this, e.g. +lanl, +llnl, etc.
        # use this for LANL builds, but for LLNL builds, we need:
        #     "--with-platform=contrib/platform/llnl/optimized"
        if self.version == ver("1.6.5") and '+lanl' in spec:
            config_args.append("--with-platform=contrib/platform/lanl/tlcc2/optimized-nopanasas")  # NOQA: ignore=E501

        configure(*config_args)
        make()
        make("install")

        self.filter_compilers()

    def filter_compilers(self):
        """Run after install to make the MPI compilers use the
           compilers that Spack built the package with.

           If this isn't done, they'll have CC, CXX and FC set
           to Spack's generic cc, c++ and f90.  We want them to
           be bound to whatever compiler they were built with.
        """
        kwargs = {'ignore_absent': True, 'backup': False, 'string': False}
        wrapper_basepath = join_path(self.prefix, 'share', 'openmpi')

        wrappers = [
            ('mpicc-vt-wrapper-data.txt', self.compiler.cc),
            ('mpicc-wrapper-data.txt', self.compiler.cc),
            ('ortecc-wrapper-data.txt', self.compiler.cc),
            ('shmemcc-wrapper-data.txt', self.compiler.cc),
            ('mpic++-vt-wrapper-data.txt', self.compiler.cxx),
            ('mpic++-wrapper-data.txt', self.compiler.cxx),
            ('ortec++-wrapper-data.txt', self.compiler.cxx),
            ('mpifort-vt-wrapper-data.txt', self.compiler.fc),
            ('mpifort-wrapper-data.txt', self.compiler.fc),
            ('shmemfort-wrapper-data.txt', self.compiler.fc),
            ('mpif90-vt-wrapper-data.txt', self.compiler.fc),
            ('mpif90-wrapper-data.txt', self.compiler.fc),
            ('mpif77-vt-wrapper-data.txt',  self.compiler.f77),
            ('mpif77-wrapper-data.txt',  self.compiler.f77)
        ]

        for wrapper_name, compiler in wrappers:
            wrapper = join_path(wrapper_basepath, wrapper_name)
            if not os.path.islink(wrapper):
                # Substitute Spack compile wrappers for the real
                # underlying compiler
                match = 'compiler=.*'
                substitute = 'compiler={compiler}'.format(compiler=compiler)
                filter_file(match, substitute, wrapper, **kwargs)
                # Remove this linking flag if present
                # (it turns RPATH into RUNPATH)
                filter_file('-Wl,--enable-new-dtags', '', wrapper, **kwargs)
