##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os

from spack import *

from spack.package import InstallError


class IntelParallelStudio(IntelPackage):
    """Intel Parallel Studio."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # As of roughly 2017, the product comes in three "editions" that vary by
    # scope.
    #
    # In Spack, select the edition via the version number in the spec, e.g.:
    #   intel-parallel-studio@cluster.2018
    #
    # NB: Download packages for some pre-2018 versions are actually the same
    # across editions, with differences apparent only from the tokens present
    # in the license file obtained as part of the purchase.

    # Cluster Edition (top; all components included)
    version('professional.2018.1', '91669ff7afbfd07868a429a122c90357', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12375/parallel_studio_xe_2018_update1_professional_edition.tgz')
    version('professional.2018.0', '9a233854e9218937bc5f46f02b3c7542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12062/parallel_studio_xe_2018_professional_edition.tgz')
    version('professional.2017.4', '27398416078e1e4005afced3e9a6df7e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('professional.2017.3', '691874735458d3e88fe0bcca4438b2a9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('professional.2017.2', '70e54b33d940a1609ff1d35d3c56e3b3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('professional.2017.1', '7f75a4a7e2c563be778c377f9d35a542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('professional.2017.0', '34c98e3329d6ac57408b738ae1daaa01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('professional.2016.4', '16a641a06b156bb647c8a56e71f3bb33', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('professional.2015.6', 'd460f362c30017b60f85da2e51ad25bf', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')

    # Professional Edition (middle; excluded: MPI/TAC/Cluster Checker)
    version('cluster.2018.1',      '9c007011e0e3fc72747b58756fbf01cd', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12374/parallel_studio_xe_2018_update1_cluster_edition.tgz')
    version('cluster.2018.0',      'fa9baeb83dd2e8e4a464e3db38f28d0f', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12058/parallel_studio_xe_2018_cluster_edition.tgz')
    version('cluster.2017.5',      'baeb8e584317fcdf1f60b8208bd4eab5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12138/parallel_studio_xe_2017_update5.tgz')
    version('cluster.2017.4',      '27398416078e1e4005afced3e9a6df7e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('cluster.2017.3',      '691874735458d3e88fe0bcca4438b2a9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('cluster.2017.2',      '70e54b33d940a1609ff1d35d3c56e3b3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('cluster.2017.1',      '7f75a4a7e2c563be778c377f9d35a542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('cluster.2017.0',      '34c98e3329d6ac57408b738ae1daaa01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    version('cluster.2016.4',      '16a641a06b156bb647c8a56e71f3bb33', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('cluster.2016.3',      'eda19bb0d0d19709197ede58f13443f3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('cluster.2016.2',      '70be832f2d34c9bf596a5e99d5f2d832', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('cluster.2015.6',      'd460f362c30017b60f85da2e51ad25bf', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')

    # Composer version (basic; excluded: MPI/..., Advisor/Inspector/Vtune)
    version('composer.2018.1',     '28cb807126d713350f4aa6f9f167448a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz')
    version('composer.2018.0',     '31ba768fba6e7322957b03feaa3add28', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12067/parallel_studio_xe_2018_composer_edition.tgz')
    version('composer.2017.4',     'd03d351809e182c481dc65e07376d9a2', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('composer.2017.3',     '52344df122c17ddff3687f84ceb21623', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('composer.2017.2',     '2891ab1ece43eb61b6ab892f07c47f01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('composer.2017.1',     '1f31976931ed8ec424ac7c3ef56f5e85', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('composer.2017.0',     'b67da0065a17a05f110ed1d15c3c6312', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    version('composer.2016.4',     '2bc9bfc9be9c1968a6e42efb4378f40e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('composer.2016.3',     '3208eeabee951fc27579177b593cefe9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('composer.2016.2',     '1133fb831312eb519f7da897fec223fa', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')
    version('composer.2015.6',     'da9f8600c18d43d58fba0488844f79c9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8432/l_compxe_2015.6.233.tgz')

    # Generic Variants
    variant('rpath',    default=True,
            description='Add rpath to .cfg files')
    variant('newdtags', default=False,
            description='Allow use of --enable-new-dtags in MPI wrappers')
    variant('shared',   default=True,
            description='Builds shared library')
    variant('ilp64',    default=False,
            description='64 bit integers')
    variant(
        'threads', default='none',
        description='Multithreading support',
        values=('openmp', 'none'),
        multi=False
    )

    # Components available in all editions
    variant('daal', default=True,
            description='Install the Intel DAAL libraries')
    variant('gdb',  default=False,
            description='Install the Intel Debugger for Heterogeneous Compute')
    variant('ipp',  default=True,
            description='Install the Intel IPP libraries')
    variant('mkl',  default=True,
            description='Install the Intel MKL library')
    variant('mpi',  default=True,
            description='Install the Intel MPI library')
    variant('tbb',  default=True,
            description='Install the Intel TBB libraries')

    # Components only available in the Professional and Cluster Editions
    variant('advisor',   default=False,
            description='Install the Intel Advisor')
    variant('clck',      default=False,
            description='Install the Intel Cluster Checker')
    variant('inspector', default=False,
            description='Install the Intel Inspector')
    variant('itac',      default=False,
            description='Install the Intel Trace Analyzer and Collector')
    variant('vtune',     default=False,
            description='Install the Intel VTune Amplifier XE')

    provides('daal', when='+daal')

    provides('ipp', when='+ipp')

    provides('mkl',       when='+mkl')
    provides('blas',      when='+mkl')
    provides('lapack',    when='+mkl')
    provides('scalapack', when='+mkl')

    provides('mpi', when='+mpi')

    provides('tbb', when='+tbb')

    # The following components are not available in the Composer Edition
    conflicts('+advisor',   when='@composer.0:composer.9999')
    conflicts('+clck',      when='@composer.0:composer.9999')
    conflicts('+inspector', when='@composer.0:composer.9999')
    conflicts('+itac',      when='@composer.0:composer.9999')
    conflicts('+vtune',     when='@composer.0:composer.9999')

    @property
    def components(self):
        spec = self.spec
        edition = self.version[0]

        # Intel(R) Compilers
        components = [
            # Common files
            'intel-comp-',
            'intel-openmp',

            # C/C++
            'intel-icc',

            # Fortran
            'intel-ifort',

            # Parallel Studio Documentation and Licensing Files
            'intel-psxe',
        ]

        # Intel(R) Parallel Studio XE Suite Files and Documentation
        if edition == 'cluster':
            components.append('intel-icsxe')
        elif edition == 'professional':
            components.extend(['intel-ips', 'intel-ipsc', 'intel-ipsf'])
        elif edition == 'composer':
            components.extend([
                'intel-compxe', 'intel-ccompxe', 'intel-fcompxe'
            ])

        # Intel(R) Data Analytics Acceleration Library
        if '+daal' in spec:
            components.append('intel-daal')

        # Intel(R) Debugger for Heterogeneous Compute
        if '+gdb' in spec:
            components.append('intel-gdb')

        # Intel(R) Integrated Performance Primitives
        if '+ipp' in spec:
            components.extend(['intel-ipp', 'intel-crypto-ipp'])

        # Intel(R) Math Kernel Library
        if '+mkl' in spec:
            components.append('intel-mkl')

        # Intel(R) MPI Library
        if '+mpi' in spec:
            components.extend(['intel-mpi', 'intel-mpirt', 'intel-imb'])

        # Intel(R) Threading Building Blocks
        if '+tbb' in spec:
            components.append('intel-tbb')

        # Intel(R) Advisor
        if '+advisor' in spec:
            components.append('intel-advisor')

        # Intel(R) Cluster Checker
        if '+clck' in spec:
            components.append('intel_clck')

        # Intel(R) Inspector
        if '+inspector' in spec:
            components.append('intel-inspector')

        # Intel(R) Trace Analyzer and Collector
        if '+itac' in spec:
            components.extend(['intel-itac', 'intel-ta', 'intel-tc'])

        # Intel(R) VTune(TM) Amplifier XE
        if '+vtune' in spec:
            components.append('intel-vtune-amplifier')

        return components

    @property
    def file_to_source(self):
        return join_path(self.studio_dir, 'bin', 'psxevars.sh')

    @property
    def license_files(self):
        spec = self.spec
        year = self.version[1]

        directories = [
            'Licenses',
            self.component_bin_dir(component='compiler', relative=True)
        ]

        if '+advisor' in spec:
            advisor_dir = 'advisor_xe/licenses'

            if year >= 2017:
                advisor_dir = 'advisor/licenses'

            directories.append(advisor_dir)

        if '+inspector' in spec:
            inspector_dir = 'inspector_xe/licenses'

            if year >= 2017:
                inspector_dir = 'inspector/licenses'

            directories.append(inspector_dir)

        if '+itac' in spec:
            itac_dir = 'itac_{0}'.format(year)

            directories.append(itac_dir)

        if '+vtune' in spec:
            vtune_dir = 'vtune_amplifier_xe/licenses'

            if year >= 2018:
                vtune_dir = 'vtune_amplifier/licenses'

            directories.append(vtune_dir)

        return [os.path.join(dir, 'license.lic') for dir in directories]

    @run_after('install')
    def filter_compiler_wrappers(self):
        spec = self.spec

        if '+mpi' in spec:
            if '~newdtags' in spec:
                wrappers = [
                    'mpif77', 'mpif90', 'mpigcc', 'mpigxx',
                    'mpiicc', 'mpiicpc', 'mpiifort'
                ]
                wrapper_paths = []
                for root, dirs, files in os.walk(spec.prefix):
                    for name in files:
                        if name in wrappers:
                            wrapper_paths.append(os.path.join(spec.prefix,
                                                              root, name))
                for wrapper in wrapper_paths:
                    filter_file('-Xlinker --enable-new-dtags', ' ',
                                wrapper, string=True)

    @run_after('install')
    def rpath_configuration(self):
        if '+rpath' not in self.spec:
            return

        # https://software.intel.com/en-us/cpp-compiler-18.0-developer-guide-and-reference-using-configuration-files
        compilers_bin_dir = self.component_bin_dir(component='compiler')
        rpath_dir = self.component_lib_dir(component='compiler')

        for compiler_name in 'icc icpc ifort'.split():
            f = os.path.join(compilers_bin_dir, compiler_name)
            if not os.path.isfile(f):
                raise InstallError(
                    'Cannot find compiler command to configure rpath:\n\t' + f)

            compiler_cfg = os.path.abspath(f + '.cfg')
            with open(compiler_cfg, 'w') as fh:
                fh.write('-Xlinker -rpath={0}\n'.format(rpath_dir))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # DUP code in var/spack/repos/builtin/packages/intel-mpi/package.py
        # Should be in parent class, but spack_cc & friends are undef'd there!?
        spack_env.set('I_MPI_CC', spack_cc)
        spack_env.set('I_MPI_CXX', spack_cxx)
        spack_env.set('I_MPI_F77', spack_fc)
        spack_env.set('I_MPI_F90', spack_f77)
        spack_env.set('I_MPI_FC', spack_fc)
        # Convenience variable.
        spack_env.set('I_MPI_ROOT', self.component_dir(component='mpi'))

    @run_after('install')
    def fix_psxevars(self):
        """Newer versions (>2016) of Intel Parallel Studio have a bug in the
        ``psxevars.sh`` script."""
# TODO: I don't think this still applies as of 2017.3 and later:
#
# $ grep "SCRIPTPATH=" parallel_studio_xe_201?.*/psxevars.sh
# par..._xe_2016.0.047/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2016.1.056/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2016.2.062/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2016.3.067/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2016.4.072/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2017.0.035/psxevars.sh:SCRIPTPATH=/opt/intel
# par..._xe_2017.3.053/psxevars.sh:SCRIPTPATH=/opt/intel/par..._xe_2017.3.053
# par..._xe_2017.4.056/psxevars.sh:SCRIPTPATH=/opt/intel/par..._xe_2017.4.056
# par..._xe_2017.5.061/psxevars.sh:SCRIPTPATH=/opt/intel/par..._xe_2017.5.061
# par..._xe_2017.6.064/psxevars.sh:SCRIPTPATH=/opt/intel/par..._xe_2017.6.064
# par..._xe_2018.1.038/psxevars.sh:SCRIPTPATH=/opt/intel/par..._xe_2018.1.038
#
# (I did not have .1 and .2 installed)

        f = self.file_to_source
        if self.version > Version('2016') and self.version < Version('2017.3'):
            filter_file('^SCRIPTPATH=.*',
                        'SCRIPTPATH={0}'.format(self.prefix),
                        f)
        # Don't bother with the csh version.
