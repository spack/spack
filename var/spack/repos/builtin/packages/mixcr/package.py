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


class Mixcr(Package):
    """MiXCR is a universal framework that processes big immunome data from
    raw sequences to quantitated clonotypes. MiXCR efficiently handles
    paired- and single-end reads, considers sequence quality, corrects PCR
    errors and identifies germline hypermutations. The software supports
    both partial- and full-length profiling and employs all available RNA or
    DNA information, including sequences upstream of V and downstream of J
    gene segments."""

    homepage = "https://mixcr.readthedocs.io/en/master/index.html"
    url      = "https://github.com/milaboratory/mixcr/releases/download/v3.0.2/mixcr-3.0.2.zip"

    version('3.0.2', sha256='b4dcad985053438d5f5590555f399edfbd8cb514e1b9717620ee0ad0b5eb6b33')

    depends_on('java@8:')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)
