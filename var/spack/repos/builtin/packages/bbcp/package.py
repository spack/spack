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


class Bbcp(Package):
    """Securely and quickly copy data from source to target"""

    homepage = "http://www.slac.stanford.edu/~abh/bbcp/"
    git      = "http://www.slac.stanford.edu/~abh/bbcp/bbcp.git"

    version('git', branch='master')

    depends_on('zlib')
    depends_on('openssl')

    def install(self, spec, prefix):
        cd("src")
        make()
        # BBCP wants to build the executable in a directory whose name depends
        # on the system type
        makesname = Executable("../MakeSname")
        bbcp_executable_path = "../bin/%s/bbcp" % makesname(
            output=str).rstrip("\n")
        destination_path = "%s/bin/" % prefix
        mkdirp(destination_path)
        install(bbcp_executable_path, destination_path)
