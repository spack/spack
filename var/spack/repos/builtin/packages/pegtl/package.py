##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


# package has a Makefile, but only to build examples
class Pegtl(CMakePackage):
    """The Parsing Expression Grammar Template Library (PEGTL) is a
        zero-dependency C++11 header-only library for creating parsers
        according to a Parsing Expression Grammar (PEG).
    """

    homepage = "https://github.com/taocpp/PEGTL"
    url      = "https://github.com/taocpp/PEGTL/tarball/2.1.4"
    git      = "https://github.com/taocpp/PEGTL.git"

    version('develop', branch='master')
    version('2.1.4', 'e5288b6968e6e910287fce93dc5557bf')
    version('2.0.0', 'c772828e7188459338a920c21f9896db')
