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


class Intel(IntelPackage):
    """Intel Compilers."""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # Same as in ../intel-parallel-studio/package.py, Composer Edition,
    # but the version numbering in Spack differs.
    version('18.0.3',              '234223cc470717c2095456d9f048d690', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13002/parallel_studio_xe_2018_update3_composer_edition.tgz')
    version('18.0.2',              '76f820f53de4c1ff998229c983cf4f53', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12722/parallel_studio_xe_2018_update2_composer_edition.tgz')
    version('18.0.1',              '28cb807126d713350f4aa6f9f167448a', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12381/parallel_studio_xe_2018_update1_composer_edition.tgz')
    version('18.0.0',              '31ba768fba6e7322957b03feaa3add28', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12067/parallel_studio_xe_2018_composer_edition.tgz')
    #
    version('17.0.7',              '4c02a4a29a8f2424f31baa23116a1001', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12860/parallel_studio_xe_2017_update7_composer_edition.tgz')
    version('17.0.6',              'd96cce0c3feef20091efde458f581a9f', url='http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12538/parallel_studio_xe_2017_update6_composer_edition.tgz')
    # version('17.0.5',              -- TBD --
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

    # Since the current package is a subset of 'intel-parallel-studio',
    # all remaining Spack actions are handled in the package class.
