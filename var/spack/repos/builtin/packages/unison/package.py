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


class Unison(Package):
    """Unison is a file-synchronization tool for OSX, Unix, and
       Windows. It allows two replicas of a collection of files and
       directories to be stored on different hosts (or different disks
       on the same host), modified separately, and then brought up to
       date by propagating the changes in each replica to the
       other."""

    homepage = "https://www.cis.upenn.edu/~bcpierce/unison/"
    url      = "https://www.seas.upenn.edu/~bcpierce/unison//download/releases/stable/unison-2.48.4.tar.gz"

    version('2.48.4', '5334b78c7e68169df7de95f4c6c4b60f')

    depends_on('ocaml', type='build')

    parallel = False

    def install(self, spec, prefix):
        make('./mkProjectInfo')
        make('UISTYLE=text')

        mkdirp(prefix.bin)
        install('unison', prefix.bin)
        set_executable(join_path(prefix.bin, 'unison'))
