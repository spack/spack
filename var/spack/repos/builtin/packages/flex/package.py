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


class Flex(AutotoolsPackage):
    """Flex is a tool for generating scanners."""

    homepage = "https://github.com/westes/flex"
    url = "https://github.com/westes/flex/archive/v2.6.2.tar.gz"

    version('2.6.2', 'acde3a89ef2b376aac94586fd5fda460')
    version('2.6.1', 'c4f31e0e4bd1711b7c91f16ef526ad90')
    version('2.6.0', '760be2ee9433e822b6eb65318311c19d')
    version('2.5.39', '5865e76ac69c05699f476515592750d7')
                
    depends_on("bison", type='build')
    depends_on("m4", type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    
    def url_for_version(self, version):
        base_url = "https://github.com/westes/flex/archive"
        if version >= Version("2.6.0"):
            return "{0}/v{1}.tar.gz".format(base_url, version)
        else:
            return "{0}/flex-{1}.tar.gz".format(base_url, version)
        
    def autoreconf(self, spec, prefix):
        autogen = Executable('./autogen.sh')
        autogen()
