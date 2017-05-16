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

from spack import *


def _verbs_dir():
    """Try to find the directory where the OpenFabrics verbs package is
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
    except TypeError:
        return None
    except ProcessError:
        return None


class Openmpi(AutotoolsPackage):
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
    url = "https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.1.tar.bz2"
    list_url = "http://www.open-mpi.org/software/ompi/"
    list_depth = 2

    version('2.1.1', 'ae542f5cf013943ffbbeb93df883731b')
    version('2.1.0', '4838a5973115c44e14442c01d3f21d52')
    version('2.0.2', 'ecd99aa436a1ca69ce936a96d6a3fa48')
    version('2.0.1', '6f78155bd7203039d2448390f3b51c96')
    version('2.0.0', 'cdacc800cb4ce690c1f1273cb6366674')
    version('1.10.6', '2e65008c1867b1f47c32f9f814d41706')
    version('1.10.5', 'd32ba9530a869d9c1eae930882ea1834')
    version('1.10.4', '9d2375835c5bc5c184ecdeb76c7c78ac')
    version('1.10.3', 'e2fe4513200e2aaa1500b762342c674b')
    version('1.10.2', 'b2f43d9635d2d52826e5ef9feb97fd4c')
    version('1.10.1', 'f0fcd77ed345b7eafb431968124ba16e')
    version('1.10.0', '280cf952de68369cebaca886c5ce0304')
    version('1.8.8', '0dab8e602372da1425e9242ae37faf8c')
    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475')

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")
    patch('configure.patch', when="@1.10.0:1.10.1")
    patch('fix_multidef_pmi_class.patch', when="@2.0.0:2.0.1")

    variant(
        'fabrics',
        default=None if _verbs_dir() is None else 'verbs',
        description='List of fabrics that are enabled',
        values=('psm', 'psm2', 'pmi', 'verbs', 'mxm'),
        multi=True
    )

    variant(
        'schedulers',
        description='List of schedulers for which support is enabled',
        values=('alps', 'lsf', 'tm', 'slurm', 'sge', 'loadleveler'),
        multi=True
    )

    # Additional support options
    variant('java', default=False, description='Build Java support')
    variant('sqlite3', default=False, description='Build SQLite3 support')
    variant('vt', default=True, description='Build VampirTrace support')
    variant('thread_multiple', default=False,
            description='Enable MPI_THREAD_MULTIPLE support')
    variant('cuda', default=False, description='Enable CUDA support')

    provides('mpi@:2.2', when='@1.6.5')
    provides('mpi@:3.0', when='@1.7.5:')
    provides('mpi@:3.1', when='@2.0.0:')

    depends_on('hwloc')
    depends_on('hwloc +cuda', when='+cuda')
    depends_on('jdk', when='+java')
    depends_on('sqlite', when='+sqlite3@:1.11')

    def url_for_version(self, version):
        return "http://www.open-mpi.org/software/ompi/v%s/downloads/openmpi-%s.tar.bz2" % (
            version.up_to(2), version)

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpi_cxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recurse=True
        )

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpic++')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpi_cxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def with_or_without_verbs(self, activated):
        # Up through version 1.6, this option was previously named
        # --with-openib
        opt = 'openib'
        # In version 1.7, it was renamed to be --with-verbs
        if self.spec.satisfies('@1.7:'):
            opt = 'verbs'
        # If the option has not been activated return
        # --without-openib or --without-verbs
        if not activated:
            return '--without-{0}'.format(opt)
        line = '--with-{0}'.format(opt)
        path = _verbs_dir()
        if (path is not None) and (path not in ('/usr', '/usr/local')):
            line += '={0}'.format(path)
        return line

    @run_before('autoreconf')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'OpenMPI requires both C and Fortran compilers!'
            )

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-shared',
            '--enable-static'
        ]
        if self.spec.satisfies('@2.0:'):
            # for Open-MPI 2.0:, C++ bindings are disabled by default.
            config_args.extend(['--enable-mpi-cxx'])

        # Fabrics and schedulers
        config_args.extend(self.with_or_without('fabrics'))
        config_args.extend(self.with_or_without('schedulers'))

        # Hwloc support
        if spec.satisfies('@1.5.2:'):
            config_args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))

        # Java support
        if spec.satisfies('@1.7.4:'):
            if '+java' in spec:
                config_args.extend([
                    '--enable-java',
                    '--enable-mpi-java',
                    '--with-jdk-dir={0}'.format(spec['jdk'].prefix)
                ])
            else:
                config_args.extend([
                    '--disable-java',
                    '--disable-mpi-java'
                ])

        # SQLite3 support
        if spec.satisfies('@1.7.3:1.999'):
            if '+sqlite3' in spec:
                config_args.append('--with-sqlite3')
            else:
                config_args.append('--without-sqlite3')

        # VampirTrace support
        if spec.satisfies('@1.3:1.999'):
            if '+vt' not in spec:
                config_args.append('--enable-contrib-no-build=vt')

        # Multithreading support
        if spec.satisfies('@1.5.4:'):
            if '+thread_multiple' in spec:
                config_args.append('--enable-mpi-thread-multiple')
            else:
                config_args.append('--disable-mpi-thread-multiple')

        # CUDA support
        if spec.satisfies('@1.6:'):
            if '+cuda' in spec:
                config_args.append('--with-cuda={0}'.format(
                    spec['cuda'].prefix))
                config_args.append('--with-cuda-libdir={0}'.format(
                    spec['cuda'].libs.directories))
            else:
                config_args.append('--without-cuda')

        return config_args

    @run_after('install')
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
