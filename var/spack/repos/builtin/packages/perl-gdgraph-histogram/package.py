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


class PerlGdgraphHistogram(PerlPackage):
    """GD::Graph::histogram extends the GD::Graph module to create histograms.
       The module allow creation of count or percentage histograms."""

    homepage = "https://metacpan.org/pod/GD::Graph::histogram"
    url      = "https://cpan.metacpan.org/authors/id/W/WH/WHIZDOG/GDGraph-histogram-1.1.tar.gz"

    version('1.1', sha256='20f752d0e6deb59b29aa2ec3496b5883476d00280b6e83f5b47c33fac4097f8a')
