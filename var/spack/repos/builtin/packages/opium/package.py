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


class Opium(Package):
    """DFT pseudopotential generation project"""

    homepage = "https://opium.sourceforge.net/index.html"
    url = "https://downloads.sourceforge.net/project/opium/opium/opium-v3.8/opium-v3.8-src.tgz"

    version('3.8', 'f710c0f869e70352b4a510c31e13bf9f')

    depends_on('blas')
    depends_on('lapack')

    def install(self, spec, prefix):
        libs = spec['lapack'].libs + spec['blas'].libs
        options = ['LDFLAGS=%s' % libs.ld_flags]

        configure(*options)
        with working_dir("src", create=False):
            make("all-subdirs")
            make("opium")

        # opium not have a make install :-((
        mkdirp(self.prefix.bin)
        install(join_path(self.stage.source_path, 'opium'),
                self.prefix.bin)
