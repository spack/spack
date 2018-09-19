##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class PerlDbfile(PerlPackage):
    """DB_File is a module which allows Perl programs to make use of the
    facilities provided by Berkeley DB version 1.x (if you have a newer version
    of DB, see "Using DB_File with Berkeley DB version 2 or greater").
    It is assumed that you have a copy of the Berkeley DB manual pages at hand
    when reading this documentation. The interface defined here mirrors the
    Berkeley DB interface closely."""

    homepage = "https://metacpan.org/pod/DB_File"
    url      = "https://cpan.metacpan.org/authors/id/P/PM/PMQS/DB_File-1.840.tar.gz"

    version('1.840', '8a2e98d457a216840ac893913c24141e')

    depends_on('perl-extutils-makemaker', type='build')
