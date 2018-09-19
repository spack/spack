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


class Libedit(AutotoolsPackage):
    """An autotools compatible port of the NetBSD editline library"""
    homepage = "http://thrysoee.dk/editline/"
    url      = "http://thrysoee.dk/editline/libedit-20170329-3.1.tar.gz"

    version('3.1-20170329', 'c57a0690e62ef523c083598730272cfd')
    version('3.1-20160903', '0467d27684c453a351fbcefebbcb16a3')
    version('3.1-20150325', '43cdb5df3061d78b5e9d59109871b4f6')

    depends_on('ncurses')

    def url_for_version(self, version):
        url = "http://thrysoee.dk/editline/libedit-{0}-{1}.tar.gz"
        return url.format(version[-1], version.up_to(-1))
