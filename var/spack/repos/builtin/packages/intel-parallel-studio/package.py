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
from spack import *


class IntelParallelStudio(IntelPackage):
    """Intel Parallel Studio."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # As of 2016, the product comes in three "editions" that vary by scope.
    #
    # In Spack, select the edition via the version number in the spec, e.g.:
    #   intel-parallel-studio@cluster.2018

    # Cluster Edition (top tier; all components included)
    version('cluster.2018.3',      '7112837d20a100b895d9cd9ba9b6748d', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12998/parallel_studio_xe_2018_update3_cluster_edition.tgz')
    version('cluster.2018.2',      '3b8d93a3fa10869dde024b739b96a9c4', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12717/parallel_studio_xe_2018_update2_cluster_edition.tgz')
    version('cluster.2018.1',      '9c007011e0e3fc72747b58756fbf01cd', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12374/parallel_studio_xe_2018_update1_cluster_edition.tgz')
    version('cluster.2018.0',      'fa9baeb83dd2e8e4a464e3db38f28d0f', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12058/parallel_studio_xe_2018_cluster_edition.tgz')
    #
    version('cluster.2017.7',      '158461b000b31f0ef8169b6f0277bfb5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12856/parallel_studio_xe_2017_update7.tgz')
    version('cluster.2017.6',      'b0bbddeec3e78a84b967c9ca70dade77', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12534/parallel_studio_xe_2017_update6.tgz')
    version('cluster.2017.5',      'baeb8e584317fcdf1f60b8208bd4eab5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12138/parallel_studio_xe_2017_update5.tgz')
    version('cluster.2017.4',      '27398416078e1e4005afced3e9a6df7e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('cluster.2017.3',      '691874735458d3e88fe0bcca4438b2a9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('cluster.2017.2',      '70e54b33d940a1609ff1d35d3c56e3b3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('cluster.2017.1',      '7f75a4a7e2c563be778c377f9d35a542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('cluster.2017.0',      '34c98e3329d6ac57408b738ae1daaa01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    #
    version('cluster.2016.4',      '16a641a06b156bb647c8a56e71f3bb33', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('cluster.2016.3',      'eda19bb0d0d19709197ede58f13443f3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('cluster.2016.2',      '70be832f2d34c9bf596a5e99d5f2d832', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('cluster.2016.1',      '83b260ef3fcfd4e30afbeb7eb31b6b20', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8365/parallel_studio_xe_2016_update1.tgz')
    version('cluster.2016.0',      '00b4de9727a906a3aff468c26dd3f89c', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/7997/parallel_studio_xe_2016.tgz')
    #
    version('cluster.2015.6',      'd460f362c30017b60f85da2e51ad25bf', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('cluster.2015.1',      '542b78c86beff9d7b01076a7be9c6ddc', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/4992/parallel_studio_xe_2015_update1.tgz')

    # Professional Edition (middle tier; excluded: MPI/TAC/Cluster Checker)
    #
    # NB: Pre-2018 download packages for Professional are the same as for
    # Cluster; differences manifest only in the tokens present in the license
    # file delivered as part of the purchase.
    version('professional.2018.3', 'e0fb828de0a5f238f775b6122cc7e2c5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12999/parallel_studio_xe_2018_update3_professional_edition.tgz')
    version('professional.2018.2', '91ed14aeb6157d60a0ec39929d0bc778', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12718/parallel_studio_xe_2018_update2_professional_edition.tgz')
    version('professional.2018.1', '91669ff7afbfd07868a429a122c90357', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12375/parallel_studio_xe_2018_update1_professional_edition.tgz')
    version('professional.2018.0', '9a233854e9218937bc5f46f02b3c7542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12062/parallel_studio_xe_2018_professional_edition.tgz')
    #
    version('professional.2017.7', '158461b000b31f0ef8169b6f0277bfb5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12856/parallel_studio_xe_2017_update7.tgz')
    version('professional.2017.6', 'b0bbddeec3e78a84b967c9ca70dade77', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12534/parallel_studio_xe_2017_update6.tgz')
    version('professional.2017.5', 'baeb8e584317fcdf1f60b8208bd4eab5', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12138/parallel_studio_xe_2017_update5.tgz')
    version('professional.2017.4', '27398416078e1e4005afced3e9a6df7e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11537/parallel_studio_xe_2017_update4.tgz')
    version('professional.2017.3', '691874735458d3e88fe0bcca4438b2a9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11460/parallel_studio_xe_2017_update3.tgz')
    version('professional.2017.2', '70e54b33d940a1609ff1d35d3c56e3b3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11298/parallel_studio_xe_2017_update2.tgz')
    version('professional.2017.1', '7f75a4a7e2c563be778c377f9d35a542', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10973/parallel_studio_xe_2017_update1.tgz')
    version('professional.2017.0', '34c98e3329d6ac57408b738ae1daaa01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9651/parallel_studio_xe_2017.tgz')
    #
    version('professional.2016.4', '16a641a06b156bb647c8a56e71f3bb33', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9781/parallel_studio_xe_2016_update4.tgz')
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9061/parallel_studio_xe_2016_update3.tgz')
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8676/parallel_studio_xe_2016_update2.tgz')
    version('professional.2016.1', '83b260ef3fcfd4e30afbeb7eb31b6b20', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8365/parallel_studio_xe_2016_update1.tgz')
    version('professional.2016.0', '00b4de9727a906a3aff468c26dd3f89c', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/7997/parallel_studio_xe_2016.tgz')
    #
    version('professional.2015.6', 'd460f362c30017b60f85da2e51ad25bf', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8469/parallel_studio_xe_2015_update6.tgz')
    version('professional.2015.1', '542b78c86beff9d7b01076a7be9c6ddc', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/4992/parallel_studio_xe_2015_update1.tgz')

    # Composer Edition (basic tier; excluded: MPI/..., Advisor/Inspector/Vtune)
    version('composer.2018.3',     '234223cc470717c2095456d9f048d690', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13002/parallel_studio_xe_2018_update3_composer_edition.tgz')
    version('composer.2018.2',     '76f820f53de4c1ff998229c983cf4f53', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12722/parallel_studio_xe_2018_update2_composer_edition.tgz')
    version('composer.2018.1',     '28cb807126d713350f4aa6f9f167448a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz')
    version('composer.2018.0',     '31ba768fba6e7322957b03feaa3add28', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12067/parallel_studio_xe_2018_composer_edition.tgz')
    #
    version('composer.2017.7',     '4c02a4a29a8f2424f31baa23116a1001', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12860/parallel_studio_xe_2017_update7_composer_edition.tgz')
    version('composer.2017.6',     'd96cce0c3feef20091efde458f581a9f', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12538/parallel_studio_xe_2017_update6_composer_edition.tgz')
    # version('composer.2017.5',     -- TBD --
    version('composer.2017.4',     'd03d351809e182c481dc65e07376d9a2', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('composer.2017.3',     '52344df122c17ddff3687f84ceb21623', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('composer.2017.2',     '2891ab1ece43eb61b6ab892f07c47f01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('composer.2017.1',     '1f31976931ed8ec424ac7c3ef56f5e85', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('composer.2017.0',     'b67da0065a17a05f110ed1d15c3c6312', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    #
    version('composer.2016.4',     '2bc9bfc9be9c1968a6e42efb4378f40e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('composer.2016.3',     '3208eeabee951fc27579177b593cefe9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('composer.2016.2',     '1133fb831312eb519f7da897fec223fa', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')
    #
    # Pre-2016, the only product was "Composer XE"; dir structure is different.
    version('composer.2015.6',     'da9f8600c18d43d58fba0488844f79c9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8432/l_compxe_2015.6.233.tgz')
    version('composer.2015.1',     '85beae681ae56411a8e791a7c44a5c0a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/4933/l_compxe_2015.1.133.tgz')

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

    provides('daal',        when='+daal')
    provides('ipp',         when='+ipp')

    provides('mkl',         when='+mkl')
    provides('blas',        when='+mkl')
    provides('lapack',      when='+mkl')
    provides('scalapack',   when='+mkl')

    provides('mpi',         when='+mpi')
    provides('tbb',         when='+tbb')

    # For TBB, static linkage is not and has never been supported by Intel:
    # https://www.threadingbuildingblocks.org/faq/there-version-tbb-provides-statically-linked-libraries
    conflicts('+tbb',       when='~shared')

    conflicts('+advisor',   when='@composer.0:composer.9999')
    conflicts('+clck',      when='@composer.0:composer.9999')
    conflicts('+inspector', when='@composer.0:composer.9999')
    conflicts('+itac',      when='@composer.0:composer.9999')
    conflicts('+mpi',       when='@composer.0:composer.9999')
    conflicts('+vtune',     when='@composer.0:composer.9999')

    conflicts('+clck',      when='@professional.0:professional.9999')
    conflicts('+itac',      when='@professional.0:professional.9999')
    conflicts('+mpi',       when='@professional.0:professional.9999')

    # The following components are not available before 2016
    conflicts('+daal',      when='@professional.0:professional.2015.7')
    conflicts('+daal',      when='@cluster.0:cluster.2015.7')
    conflicts('+daal',      when='@composer.0:composer.2015.7')

    def setup_dependent_environment(self, *args):
        # Handle in callback, conveying client's compilers in additional arg.
        # CAUTION - DUP code in:
        #   ../intel-mpi/package.py
        #   ../intel-parallel-studio/package.py
        self._setup_dependent_env_callback(*args, compilers_of_client={
            'CC':   spack_cc,
            'CXX':  spack_cxx,
            'F77':  spack_f77,
            'F90':  spack_fc,
            'FC':   spack_fc,
        })
