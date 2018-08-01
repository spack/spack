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


class RAffyrnadegradation(RPackage):
    """The package helps with the assessment and correction of
    RNA degradation effects in Affymetrix 3' expression arrays.
    The parameter d gives a robust and accurate measure of RNA
    integrity. The correction removes the probe positional bias,
    and thus improves comparability of samples that are affected
    by RNA degradation."""

    homepage = "https://www.bioconductor.org/packages/AffyRNADegradation/"
    git      = "https://git.bioconductor.org/packages/AffyRNADegradation.git"

    version('1.22.0', commit='0fa78f8286494711a239ded0ba587b0de47c15d3')

    depends_on('r@3.4.0:3.4.9', when='@1.22.0')
    depends_on('r-affy', type=('build', 'run'))
