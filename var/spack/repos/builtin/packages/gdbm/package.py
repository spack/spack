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
#
from spack import *


class Gdbm(AutotoolsPackage):
    """GNU dbm (or GDBM, for short) is a library of database functions
    that use extensible hashing and work similar to the standard UNIX dbm.
    These routines are provided to a programmer needing to create and
    manipulate a hashed database."""

    homepage = "http://www.gnu.org.ua/software/gdbm/gdbm.html"
    url      = "https://ftpmirror.gnu.org/gdbm/gdbm-1.13.tar.gz"

    version('1.14.1', 'c2ddcb3897efa0f57484af2bd4f4f848')
    version('1.13',  '8929dcda2a8de3fd2367bdbf66769376')
    version('1.12',  '9ce96ff4c99e74295ea19040931c8fb9')
    version('1.11',  '72c832680cf0999caedbe5b265c8c1bd')
    version('1.10',  '88770493c2559dc80b561293e39d3570')
    version('1.9.1', '59f6e4c4193cb875964ffbe8aa384b58')
    version('1.9',   '1f0e8e6691edd61bdd6b697b8c02528d')

    depends_on("readline")

    def configure_args(self):

        # GDBM uses some non-standard GNU extensions,
        # enabled with -D_GNU_SOURCE.  See:
        #   https://patchwork.ozlabs.org/patch/771300/
        #   https://stackoverflow.com/questions/5582211
        #   https://www.gnu.org/software/automake/manual/html_node/Flag-Variables-Ordering.html
        return [
            '--enable-libgdbm-compat',
            'CPPFLAGS=-D_GNU_SOURCE']
