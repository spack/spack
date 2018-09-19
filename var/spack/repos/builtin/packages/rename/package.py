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


class Rename(Package):
    """Perl-powered file rename script with many helpful built-ins."""

    homepage = "http://plasmasturm.org/code/rename"
    url      = "https://github.com/ap/rename/archive/v1.600.tar.gz"

    version('1.600', '91beb555c93d407420b5dad191069bb3')

    depends_on('perl', type=('build', 'run'))

    def install(self, spec, prefix):
        Executable('pod2man')('rename', 'rename.1')
        bdir = join_path(prefix, 'bin')
        mkdirp(bdir)
        install('rename', bdir)
        mdir = join_path(prefix, 'share', 'man', 'man1')
        mkdirp(mdir)
        install('rename.1', mdir)
