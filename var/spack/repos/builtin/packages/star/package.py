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


class Star(Package):
    """STAR is an ultrafast universal RNA-seq aligner."""

    homepage = "https://github.com/alexdobin/STAR"
    url      = "https://github.com/alexdobin/STAR/archive/2.6.1a.tar.gz"

    version('2.6.1a', '1ebaac553809c20900e0b42aadf75cc6')
    version('2.5.3a', 'baf8d1b62a50482cfa13acb7652dc391')
    version('2.4.2a', '8b9345f2685a5ec30731e0868e86d506',
            url='https://github.com/alexdobin/STAR/archive/STAR_2.4.2a.tar.gz')

    depends_on('zlib')

    def install(self, spec, prefix):
        with working_dir('source'):
            make('STAR', 'STARlong')
            mkdirp(prefix.bin)
            install('STAR', prefix.bin)
            install('STARlong', prefix.bin)
