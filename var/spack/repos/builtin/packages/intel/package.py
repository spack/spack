# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Intel(IntelPackage):
    """Intel Compilers."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # Same as in ../intel-parallel-studio/package.py, Composer Edition,
    # but the version numbering in Spack differs.
    version('19.0.4',              '1915993445323e1e78d6de73702a88fa3df2036109cde03d74ee38fef9f1abf2', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15537/parallel_studio_xe_2019_update4_composer_edition.tgz')
    version('19.0.3',              '15373ac6df2a84e6dd9fa0eac8b5f07ab00cdbb67f494161fd0d4df7a71aff8e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/15272/parallel_studio_xe_2019_update3_composer_edition.tgz')
    version('19.0.1',              'db000cb2ebf411f6e91719db68a0c68b8d3f7d38ad7f2049ea5b2f1b5f006c25', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14832/parallel_studio_xe_2019_update1_composer_edition.tgz')
    version('19.0.0',              'e1a29463038b063e01f694e2817c0fcf1a8e824e24f15a26ce85f20afa3f963a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13581/parallel_studio_xe_2019_composer_edition.tgz')
    #
    version('18.0.4',              '94aca8f091dff9535b02f022a37aef150b36925c8ef069335621496f8e4db267', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13722/parallel_studio_xe_2018_update4_composer_edition.tgz')
    version('18.0.3',              '234223cc470717c2095456d9f048d690', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13002/parallel_studio_xe_2018_update3_composer_edition.tgz')
    version('18.0.2',              '76f820f53de4c1ff998229c983cf4f53', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12722/parallel_studio_xe_2018_update2_composer_edition.tgz')
    version('18.0.1',              '28cb807126d713350f4aa6f9f167448a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz')
    version('18.0.0',              '31ba768fba6e7322957b03feaa3add28', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12067/parallel_studio_xe_2018_composer_edition.tgz')
    #
    version('17.0.7',              '4c02a4a29a8f2424f31baa23116a1001', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12860/parallel_studio_xe_2017_update7_composer_edition.tgz')
    version('17.0.6',              'd96cce0c3feef20091efde458f581a9f', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12538/parallel_studio_xe_2017_update6_composer_edition.tgz')
    version('17.0.5',              'ede4ea9351fcf263103588ae0f130b4c2a79395529cdb698b0d6e866c4871f78', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12144/parallel_studio_xe_2017_update5_composer_edition.tgz')
    version('17.0.4',              'd03d351809e182c481dc65e07376d9a2', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11541/parallel_studio_xe_2017_update4_composer_edition.tgz')
    version('17.0.3',              '52344df122c17ddff3687f84ceb21623', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11464/parallel_studio_xe_2017_update3_composer_edition.tgz')
    version('17.0.2',              '2891ab1ece43eb61b6ab892f07c47f01', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/11302/parallel_studio_xe_2017_update2_composer_edition.tgz')
    version('17.0.1',              '1f31976931ed8ec424ac7c3ef56f5e85', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/10978/parallel_studio_xe_2017_update1_composer_edition.tgz')
    version('17.0.0',              'b67da0065a17a05f110ed1d15c3c6312', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9656/parallel_studio_xe_2017_composer_edition.tgz')
    #
    version('16.0.4',              '2bc9bfc9be9c1968a6e42efb4378f40e', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9785/parallel_studio_xe_2016_composer_edition_update4.tgz')
    version('16.0.3',              '3208eeabee951fc27579177b593cefe9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/9063/parallel_studio_xe_2016_composer_edition_update3.tgz')
    version('16.0.2',              '1133fb831312eb519f7da897fec223fa', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8680/parallel_studio_xe_2016_composer_edition_update2.tgz')
    #
    # Grandfathered release; different directory structure.
    version('15.0.6',              'da9f8600c18d43d58fba0488844f79c9', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/8432/l_compxe_2015.6.233.tgz')
    version('15.0.1',              '85beae681ae56411a8e791a7c44a5c0a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/4933/l_compxe_2015.1.133.tgz')

    variant('rpath', default=True, description='Add rpath to .cfg files')

    auto_dispatch_options = IntelPackage.auto_dispatch_options
    variant(
        'auto_dispatch',
        values=any_combination_of(*auto_dispatch_options),
        description='Enable generation of multiple auto-dispatch code paths'
    )

    # MacOS does not support some of the auto dispatch settings
    conflicts('auto_dispatch=SSE2', 'platform=darwin',
              msg='SSE2 is not supported on MacOS')
    conflicts('auto_dispatch=SSE3', 'platform=darwin target=x86_64:',
              msg='SSE3 is not supported on MacOS x86_64')

    # Since the current package is a subset of 'intel-parallel-studio',
    # all remaining Spack actions are handled in the package class.
