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


class Tut(WafPackage):
    """TUT is a small and portable unit test framework for C++."""

    homepage = "http://mrzechonek.github.io/tut-framework/"
    url      = "https://github.com/mrzechonek/tut-framework/tarball/2016-12-19"

    version('2016-12-19', '8b1967fa295ae1ce4d4431c2f811e521')

    patch('python3-octal.patch', when='@2016-12-19')

    def build_args(self):
        args = []

        if self.run_tests:
            # Run unit tests
            args.append('--test')

        return args
