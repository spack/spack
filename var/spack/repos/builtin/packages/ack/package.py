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


class Ack(Package):
    """ack 2.14 is a tool like grep, optimized for programmers.

       Designed for programmers with large heterogeneous trees of
       source code, ack is written purely in portable Perl 5 and takes
       advantage of the power of Perl's regular expressions."""

    homepage = "http://beyondgrep.com/"
    url      = "http://beyondgrep.com/ack-2.14-single-file"

    version('2.22', 'eea9d4daef7c262751f15ca9b3b70317', expand=False)
    version('2.18', 'e8ebfd7a7ec8476bffd4686bf7b14fd7', expand=False)
    version('2.16', '7085b5a5c76fda43ff049410870c8535', expand=False)
    version('2.14', 'e74150a1609d28a70b450ef9cc2ed56b', expand=False)

    depends_on('perl')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        ack = 'ack-{0}-single-file'.format(self.version)

        # rewrite the script's #! line to call the perl dependency
        shbang = '#!' + spec['perl'].command.path
        filter_file(r'^#!/usr/bin/env perl', shbang, ack)

        install(ack, join_path(prefix.bin, "ack"))
        set_executable(join_path(prefix.bin, "ack"))
