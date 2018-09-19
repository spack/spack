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


class Mpest(MakefilePackage):
    """MP-EST estimates species trees from a set of gene trees by maximizing
       a pseudo-likelihood function."""

    homepage = "http://faculty.franklin.uga.edu/lliu/content/mp-est"
    url      = "https://faculty.franklin.uga.edu/lliu/sites/faculty.franklin.uga.edu.lliu/files/mpest_1.5.zip"

    version('1.5', 'f176d5301aa26567918664e5e30027d1')

    @property
    def build_directory(self):
        return join_path('mpest_{0}'.format(self.version), 'src')

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install('mpest', prefix.bin)

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('platform=darwin'):
            spack_env.set('ARCHITECTURE', 'mac')
        else:
            spack_env.set('ARCHITECTURE', 'unix')
