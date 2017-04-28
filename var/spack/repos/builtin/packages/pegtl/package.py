##############################################################################
# Copyright (c) 2017, Los Alamos National Security, LLC
# Produced at the Los Alamos National Laboratory.
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


# package has a Makefile, but only to build examples
class Pegtl(Package):
    """The Parsing Expression Grammar Template Library (PEGTL) is a
        zero-dependency C++11 header-only library for creating parsers
        according to a Parsing Expression Grammar (PEG).
    """

    homepage = "https://github.com/taocpp/PEGTL"
    url      = "https://github.com/taocpp/PEGTL/tarball/1.3.1"

    version('1.3.1', '11efc4beac8f4f5153466d56074e9f0c')

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree('pegtl', join_path(prefix.include, 'pegtl'))
        install('pegtl.hh', prefix.include)
