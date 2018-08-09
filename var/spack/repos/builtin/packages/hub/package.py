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
import os


class Hub(Package):
    """The github git wrapper"""

    homepage = "https://github.com/github/hub"
    url      = "https://github.com/github/hub/archive/v2.2.3.tar.gz"
    git      = "https://github.com/github/hub.git"

    version('head', branch='master')
    version('2.2.3', '6675992ddd16d186eac7ba4484d57f5b')
    version('2.2.2', '7edc8f5b5d3c7c392ee191dd999596fc')
    version('2.2.1', '889a31ee9d10ae9cb333480d8dbe881f')
    version('2.2.0', 'eddce830a079b8480f104aa7496f46fe')
    version('1.12.4', '4f2ebb14834c9981b04e40b0d1754717')

    extends("go")

    def install(self, spec, prefix):
        env = os.environ
        env['GOPATH'] = self.stage.source_path + ':' + env['GOPATH']
        bash = which('bash')
        bash(os.path.join('script', 'build'), '-o', os.path.join(prefix, 'bin',
                                                                 'hub'))
