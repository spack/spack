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


class Shortbred(Package):
    """ShortBRED is a system for profiling protein families of interest at
    very high specificity in shotgun meta'omic sequencing data."""

    homepage = "https://huttenhower.sph.harvard.edu/shortbred"
    url      = "https://bitbucket.org/biobakery/shortbred/get/0.9.4.tar.gz"

    version('0.9.4', 'ad3dff344cbea3713e78b384afad28fd')

    depends_on('blast-plus@2.2.28:')
    depends_on('cdhit@4.6:')
    depends_on('muscle@3.8.31:')
    depends_on('python@2.7.9:')
    depends_on('py-biopython')
    depends_on('usearch@6.0.307:')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('shortbred_identify.py', prefix.bin)
        install('shortbred_quantify.py', prefix.bin)
        install_tree('src', prefix.src)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PYTHONPATH', self.prefix)
