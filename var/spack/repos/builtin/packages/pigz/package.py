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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install pigz
#
# You can edit this file again by typing:
#
#     spack edit pigz
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Pigz(Package):
    """A parallel implementation of gzip for modern multi-processor, multi-core machines."""

    homepage = "http://zlib.net/pigz/"
    url      = "http://zlib.net/pigz/pigz-2.3.4.tar.gz"

    version('2.3.4', '08e6b2e682bbf65ccf12c8966d633fc6')

    depends_on('zlib')

    def install(self, spec, prefix):
        make()
        mkdirp(prefix.bin)
	mkdirp(prefix.man1)
	install('pigz', "%s/pigz" % prefix.bin)
	install('pigz.1', "%s/pigz.1" % prefix.man1)
