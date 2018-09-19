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


class Preseq(MakefilePackage):
    """The preseq package is aimed at predicting and estimating the complexity
       of a genomic sequencing library, equivalent to predicting and
       estimating the number of redundant reads from a given sequencing depth
       and how many will be expected from additional sequencing using an
       initial sequencing experiment."""

    homepage = "https://github.com/smithlabcode/preseq"
    url      = "https://github.com/smithlabcode/preseq/releases/download/v2.0.2/preseq_v2.0.2.tar.bz2"

    version('2.0.2', '9f2a7b597c9f08b821db6ee55e2ea39c')

    depends_on('samtools')
    depends_on('gsl')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('PREFIX', self.prefix)
