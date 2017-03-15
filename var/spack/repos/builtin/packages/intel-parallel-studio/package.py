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
import os
import re

from spack.pkg.builtin.intel import IntelInstaller, filter_pick, \
    get_all_components


class IntelParallelStudio(IntelInstaller):
    """Intel Parallel Studio.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    version('professional.2017.2', '70e54b33d940a1609ff1d35d3c56e3b3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('cluster.2017.2',      '70e54b33d940a1609ff1d35d3c56e3b3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('composer.2017.2',     '2891ab1ece43eb61b6ab892f07c47f01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('professional.2017.1', '7f75a4a7e2c563be778c377f9d35a542',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('cluster.2017.1',      '7f75a4a7e2c563be778c377f9d35a542',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('composer.2017.1',     '1f31976931ed8ec424ac7c3ef56f5e85',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('professional.2017.0', '34c98e3329d6ac57408b738ae1daaa01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('cluster.2017.0',      '34c98e3329d6ac57408b738ae1daaa01',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('composer.2017.0',     'b67da0065a17a05f110ed1d15c3c6312',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    version('professional.2016.4', '16a641a06b156bb647c8a56e71f3bb33',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('cluster.2016.4',      '16a641a06b156bb647c8a56e71f3bb33',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('composer.2016.4',      '2bc9bfc9be9c1968a6e42efb4378f40e',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('cluster.2016.3',      'eda19bb0d0d19709197ede58f13443f3',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('composer.2016.3',     '3208eeabee951fc27579177b593cefe9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('cluster.2016.2',      '70be832f2d34c9bf596a5e99d5f2d832',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('composer.2016.2',     '1133fb831312eb519f7da897fec223fa',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')
    version('professional.2015.6', 'd460f362c30017b60f85da2e51ad25bf',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('cluster.2015.6',      'd460f362c30017b60f85da2e51ad25bf',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('composer.2015.6',      'da9f8600c18d43d58fba0488844f79c9',
            url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8432/l_compxe_2015.6.233.tgz')

    variant('rpath', default=True, description="Add rpath to .cfg files")
    variant('newdtags', default=False,
            description="Allow use of --enable-new-dtags in MPI wrappers")
    variant('all', default=False,
            description="Install all files with the requested edition")
    variant('mpi', default=True,
            description="Install the Intel MPI library and ITAC tool")
    variant('mkl', default=True, description="Install the Intel MKL library")
    variant('daal',
            default=True, description="Install the Intel DAAL libraries")
    variant('ipp', default=True, description="Install the Intel IPP libraries")
    variant('tools', default=True, description="Install the Intel Advisor, "
            "VTune Amplifier, and Inspector tools")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant('openmp', default=False, description='OpenMP multithreading layer')

    provides('mpi', when='@cluster:+mpi')
    provides('mkl', when='+mkl')
    provides('daal', when='+daal')
    provides('ipp', when='+ipp')

    # virtual dependency
    provides('blas', when='+mkl')
    provides('lapack', when='+mkl')
    provides('scalapack', when='+mkl')

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        suffix = dso_suffix if '+shared' in self.spec else 'a'
        mkl_integer = ['libmkl_intel_ilp64'] if '+ilp64' in self.spec else ['libmkl_intel_lp64']  # NOQA: ignore=E501
        mkl_threading = ['libmkl_sequential']
        if '+openmp' in self.spec:
            mkl_threading = ['libmkl_intel_thread', 'libiomp5'] if '%intel' in self.spec else ['libmkl_gnu_thread']  # NOQA: ignore=E501
        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']
        mkl_libs = find_libraries(
            mkl_integer + ['libmkl_core'] + mkl_threading,
            root=join_path(self.prefix, 'mkl', 'lib', 'intel64'),
            shared=shared
        )
        system_libs = [
            'libpthread.{0}'.format(suffix),
            'libm.{0}'.format(suffix),
            'libdl.{0}'.format(suffix)
        ]
        return mkl_libs + system_libs

    @property
    def lapack_libs(self):
        return self.libs

    @property
    def scalapack_libs(self):
        libnames = ['libmkl_scalapack']
        if self.spec.satisfies('^openmpi'):
            libnames.append('libmkl_blacs_openmpi')
        elif self.spec.satisfies('^mpich@1'):
            libnames.append('libmkl_blacs')
        elif self.spec.satisfies('^mpich@2:'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mvapich2'):
            libnames.append('libmkl_blacs_intelmpi')
        elif self.spec.satisfies('^mpt'):
            libnames.append('libmkl_blacs_sgimpt')
        # TODO: ^intel-parallel-studio can mean intel mpi, a compiler or a lib
        # elif self.spec.satisfies('^intel-parallel-studio'):
        #     libnames.append('libmkl_blacs_intelmpi')
        else:
            raise InstallError("No MPI found for scalapack")

        shared = True if '+shared' in self.spec else False
        integer = 'ilp64' if '+ilp64' in self.spec else 'lp64'
        libs = find_libraries(
            ['{0}_{1}'.format(l, integer) for l in libnames],
            root=join_path(self.prefix, 'mkl', 'lib', 'intel64'),
            shared=shared
        )
        return libs

    def install(self, spec, prefix):
        base_components = "ALL"  # when in doubt, install everything
        mpi_components = ""
        mkl_components = ""
        daal_components = ""
        ipp_components = ""

        if not spec.satisfies('+all'):
            all_components = get_all_components()
            regex = '(comp|openmp|intel-tbb|icc|ifort|psxe)'
            base_components = \
                filter_pick(all_components, re.compile(regex).search)
            regex = '(icsxe|imb|mpi|itac|intel-ta|intel-tc|clck)'
            mpi_components = \
                filter_pick(all_components, re.compile(regex).search)
            mkl_components = \
                filter_pick(all_components, re.compile('(mkl)').search)
            daal_components = \
                filter_pick(all_components, re.compile('(daal)').search)
            ipp_components = \
                filter_pick(all_components, re.compile('(ipp)').search)
            regex = '(gdb|vtune|inspector|advisor)'
            tool_components = \
                filter_pick(all_components, re.compile(regex).search)
            components = base_components

        if not spec.satisfies('+all'):
            if spec.satisfies('+mpi'):
                components += mpi_components
            if spec.satisfies('+mkl'):
                components += mkl_components
            if spec.satisfies('+daal'):
                components += daal_components
            if spec.satisfies('+ipp'):
                components += ipp_components
            if spec.satisfies('+tools') and (spec.satisfies('@cluster') or
                                             spec.satisfies('@professional')):
                components += tool_components

        if spec.satisfies('+all'):
            self.intel_components = 'ALL'
        else:
            self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.dirname(
            os.path.realpath(os.path.join(self.prefix.bin, "icc")))
        abslibdir = os.path.dirname(
            os.path.realpath(os.path.join(
                self.prefix.lib, "intel64", "libimf.a")))

        os.symlink(self.global_license_file, os.path.join(absbindir,
                                                          "license.lic"))
        if spec.satisfies('+tools') and (spec.satisfies('@cluster') or
                                         spec.satisfies('@professional')):
            inspector_dir = "inspector_xe/licenses"
            advisor_dir = "advisor_xe/licenses"
            vtune_amplifier_dir = "vtune_amplifier_xe/licenses"

            year = int(str(self.version).split('.')[1])
            if year >= 2017:
                inspector_dir = "inspector/licenses"
                advisor_dir = "advisor/licenses"

            os.mkdir(os.path.join(self.prefix, inspector_dir))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, inspector_dir, "license.lic"))
            os.mkdir(os.path.join(self.prefix, advisor_dir))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, advisor_dir, "license.lic"))
            os.mkdir(os.path.join(self.prefix, vtune_amplifier_dir))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, vtune_amplifier_dir, "license.lic"))

        if (spec.satisfies('+all') or spec.satisfies('+mpi')) and \
                spec.satisfies('@cluster'):
            for ifile in os.listdir(os.path.join(self.prefix, "itac")):
                if os.path.isdir(os.path.join(self.prefix, "itac", ifile)):
                    os.symlink(self.global_license_file,
                               os.path.join(self.prefix, "itac", ifile,
                                            "license.lic"))
                if os.path.isdir(os.path.join(self.prefix, "itac",
                                              ifile, "intel64")):
                    os.symlink(self.global_license_file,
                               os.path.join(self.prefix, "itac",
                                            ifile, "intel64",
                                            "license.lic"))
            if spec.satisfies('~newdtags'):
                wrappers = ["mpif77", "mpif77", "mpif90", "mpif90",
                            "mpigcc", "mpigcc", "mpigxx", "mpigxx",
                            "mpiicc", "mpiicc", "mpiicpc", "mpiicpc",
                            "mpiifort", "mpiifort"]
                wrapper_paths = []
                for root, dirs, files in os.walk(spec.prefix):
                    for name in files:
                        if name in wrappers:
                            wrapper_paths.append(os.path.join(spec.prefix,
                                                              root, name))
                for wrapper in wrapper_paths:
                    filter_file(r'-Xlinker --enable-new-dtags', r' ',
                                wrapper)

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %
                                           compiler_command)
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' % abslibdir)

        os.symlink(os.path.join(self.prefix.man, "common", "man1"),
                   os.path.join(self.prefix.man, "man1"))

    def setup_environment(self, spack_env, run_env):
        # TODO: Determine variables needed for the professional edition.

        major_ver = self.version[1]

        # Remove paths that were guessed but are incorrect for this package.
        run_env.remove_path('LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('LD_LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('CPATH',
                            join_path(self.prefix, 'include'))

        # Add the default set of variables
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'tbb', 'include'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))

        if self.spec.satisfies('+all'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix,
                                           'debugger_{0}'.format(major_ver),
                                           'libipt', 'intel64', 'lib'))
            run_env.set('GDBSERVER_MIC',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'gdb',
                                  'targets', 'mic', 'bin', 'gdbserver'))
            run_env.set('GDB_CROSS',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver),
                                  'gdb', 'intel64_mic', 'bin', 'gdb-mic'))
            run_env.set('MPM_LAUNCHER',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'mpm',
                                  'mic',
                                  'bin', 'start_mpm.sh'))
            run_env.set('INTEL_PYTHONHOME',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'python',
                                  'intel64'))

        if (self.spec.satisfies('+all') or self.spec.satisfies('+mpi')):
            # Only I_MPI_ROOT is set here because setting the various PATH
            # variables will potentially be in conflict with other MPI
            # environment modules. The I_MPI_ROOT environment variable can be
            # used as a base to set necessary PATH variables for using Intel
            # MPI. It is also possible to set the variables in the modules.yaml
            # file if Intel MPI is the dominant, or only, MPI on a system.
            run_env.set('I_MPI_ROOT', join_path(self.prefix, 'impi'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+mkl'):
            spack_env.set('MKLROOT', join_path(self.prefix, 'mkl'))

            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib',
                                           'intel64'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib',
                                           'intel64'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'mkl', 'include'))
            run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib', 'mic'))
            run_env.set('MKLROOT', join_path(self.prefix, 'mkl'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+daal'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'intel64_lin'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'intel64_lin'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'daal', 'include'))
            run_env.prepend_path('CLASSPATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'daal.jar'))
            run_env.set('DAALROOT', join_path(self.prefix, 'daal'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+ipp'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib',
                                           'intel64'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib',
                                           'intel64'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'ipp', 'include'))
            run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib', 'mic'))
            run_env.set('IPPROOT', join_path(self.prefix, 'ipp'))
