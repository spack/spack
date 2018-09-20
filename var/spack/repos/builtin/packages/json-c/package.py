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


class JsonC(AutotoolsPackage):
    """A JSON implementation in C."""
    homepage = "https://github.com/json-c/json-c/wiki"
    url      = "https://s3.amazonaws.com/json-c_releases/releases/json-c-0.12.1.tar.gz"

    version('0.13.1', '04969ad59cc37bddd83741a08b98f350')
    version('0.12.1', '55f7853f7d8cf664554ce3fa71bf1c7d')
    version('0.11',   'aa02367d2f7a830bf1e3376f77881e98')

    depends_on('autoconf', type='build')

    parallel = False

    @when('@0.12.1 %gcc@7:')
    def patch(self):
        filter_file('-Wextra',
                    '-Wextra -Wno-error=implicit-fallthrough',
                    'Makefile.in')
