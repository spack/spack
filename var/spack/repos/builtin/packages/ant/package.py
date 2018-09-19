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


class Ant(Package):
    """Apache Ant is a Java library and command-line tool whose mission is to
       drive processes described in build files as targets and extension points
       dependent upon each other
    """

    homepage = "http://ant.apache.org/"
    url = "https://archive.apache.org/dist/ant/source/apache-ant-1.9.7-src.tar.gz"

    # 1.10.0 requires newer Java, not yet tested....
    # version('1.10.0', '2260301bb7734e34d8b96f1a5fd7979c')
    version('1.9.9',  '22c9d40dabafbec348aaada226581239')
    version('1.9.8',  '16253d516d5c33c4af9ef8fafcf1004b')
    version('1.9.7',  'a2fd9458c76700b7be51ef12f07d4bb1')
    version('1.9.6',  '29b7507c9053e301d2b85091f2aec6f0')

    depends_on('java')

    def install(self, spec, prefix):
        env['ANT_HOME'] = self.prefix
        bash = which('bash')
        bash('./build.sh', 'install')
