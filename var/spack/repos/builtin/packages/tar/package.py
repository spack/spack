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


class Tar(AutotoolsPackage):
    """GNU Tar provides the ability to create tar archives, as well as various
    other kinds of manipulation."""

    homepage = "https://www.gnu.org/software/tar/"
    url = "https://ftp.gnu.org/gnu/tar/tar-1.29.tar.gz"

    version('1.29', 'cae466e6e58c7292355e7080248f244db3a4cf755f33f4fa25ca7f9a7ed09af0')
    version('1.28', '6ea3dbea1f2b0409b234048e021a9fd7')

    patch('tar-pgi.patch',    when='@1.29')
    patch('config-pgi.patch', when='@:1.29')
    patch('se-selinux.patch', when='@:1.29')
    patch('argp-pgi.patch',   when='@:1.29')
    patch('gnutar-configure-xattrs.patch', when='@1.28')
