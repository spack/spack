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


class Udunits2(AutotoolsPackage):
    """Automated units conversion"""

    homepage = "http://www.unidata.ucar.edu/software/udunits"
    url      = "https://github.com/Unidata/UDUNITS-2/archive/v2.2.23.tar.gz"

    version('2.2.25', '373106a0fcd20c40fc53a975c9fa4fca')
    version('2.2.24', '316911493e3b5c28ff7019223b4e27ea')
    version('2.2.23', '0c0d9b1ebd7ad066233bedf40e66f1ba')
    version('2.2.21', '167738b3ec886da1b92239de9cbbbc39')

    depends_on('expat')

    depends_on('bison', type='build')
    depends_on('flex',  type='build')
    depends_on('libtool', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('pkg-config', type='build')
    depends_on('texinfo', type='build')

    def autoreconf(self, spec, prefix):
        # Work around autogen.sh oddities
        # bash = which("bash")
        # bash("./autogen.sh")
        mkdirp("config")
        autoreconf = which("autoreconf")
        autoreconf("--install", "--verbose", "--force",
                   "-I", "config",
                   "-I", join_path(spec['pkg-config'].prefix,
                                   "share", "aclocal"),
                   "-I", join_path(spec['automake'].prefix,
                                   "share", "aclocal"),
                   "-I", join_path(spec['libtool'].prefix,
                                   "share", "aclocal"),
                   )
