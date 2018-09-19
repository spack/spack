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


class Soap2(Package):
    """Software for short oligonucleotide alignment."""

    homepage = "http://soap.genomics.org.cn/soapaligner.html"
    url      = "http://soap.genomics.org.cn/down/soap2.21release.tar.gz"

    version('2.21', '563b8b7235463b68413f9e841aa40779')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.share.man)
        install('soap', prefix.bin)
        install('2bwt-builder', prefix.bin)
        install('soap.1', prefix.share.man)
        install('soap.man', prefix.share.man)
