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


class Gnat(MakefilePackage):
    """The GNAT Ada compiler. Ada is a modern programming language designed
    for large, long-lived applications - and embedded systems in particular
    - where reliability and efficiency are essential."""

    homepage = "https://libre.adacore.com/tools/gnat-gpl-edition/"

    # NOTE: This is a binary installer intended to bootstrap GCC's Ada compiler

    # There may actually be a way to install GNAT from source. If you go to
    # the GNAT Download page: https://libre.adacore.com/download/
    # select "Free Software or Academic Development", select your platform,
    # expand GNAT Ada, and expand Sources, you'll see links to download the
    # source code for GNAT and all of its dependencies. Most of these
    # dependencies are already in Spack.

    # This is the GPL release for Linux x86-64
    version('2016', '9741107cca1a6a4ddb0d5e8de824a90c', extension='tar.gz',
            url="http://mirrors.cdn.adacore.com/art/5739cefdc7a447658e0b016b")

    phases = ['install']

    def install(self, spec, prefix):
        make('ins-all', 'prefix={0}'.format(prefix))
