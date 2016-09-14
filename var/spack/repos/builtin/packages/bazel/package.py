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


class Bazel(Package):
    """Bazel is Google's own build tool"""

    homepage = "https://www.bazel.io"
    url      = "https://github.com/bazelbuild/bazel/archive/0.3.1.tar.gz"

    version('0.3.1' , '5c959467484a7fc7dd2e5e4a1e8e866b')
    version('0.3.0' , '33a2cb457d28e1bee9282134769b9283')
    version('0.2.3' , '393a491d690e43caaba88005efe6da91')
    version('0.2.2b', '75081804f073cbd194da1a07b16cba5f')
    version('0.2.2' , '644bc4ea7f429d835e74f255dc1054e6')

    depends_on('jdk@8:')
    patch('fix_env_handling.patch')
    patch('link.patch')
    patch('cc_configure.patch')

    def install(self, spec, prefix):
        bash = which('bash')
        bash('-c', './compile.sh')
        mkdir(prefix.bin)
        install('output/bazel', prefix.bin)
