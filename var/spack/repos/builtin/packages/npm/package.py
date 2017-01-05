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


class Npm(Package):
    """npm: A package manager for javascript."""

    homepage = "https://github.com/npm/npm"
    # base http://www.npmjs.com/
    url      = "https://registry.npmjs.org/npm/-/npm-3.10.5.tgz"

    version('3.10.5', '46002413f4a71de9b0da5b506bf1d992')

    depends_on('node-js', type='build')

    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))

        if self.run_tests:
            make('test')

        make('install')
