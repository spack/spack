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


class Tldd(MakefilePackage):
    """A program similar to ldd(1) but showing the output as a tree."""

    homepage = "https://gitlab.com/miscripts/tldd"
    git      = "https://gitlab.com/miscripts/tldd.git"

    version('2018-10-05', commit='61cb512cc992ea6cbb7239e99ec7ac92ea072507')
    version('master', branch='master')

    depends_on('pstreams@0.8.0:')

    def patch(self):
        filter_file(
            r'#include <pstreams/pstream.h>',
            r'#include <pstream.h>',
            'tldd.cc')

    @property
    def install_targets(self):
        return ['install', 'PREFIX={0}'.format(self.prefix)]
