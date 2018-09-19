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


class RMzid(RPackage):
    """A parser for mzIdentML files implemented using the XML package. The
       parser tries to be general and able to handle all types of mzIdentML
       files with the drawback of having less 'pretty' output than a vendor
       specific parser. Please contact the maintainer with any problems and
       supply an mzIdentML file so the problems can be fixed quickly."""

    homepage = "https://www.bioconductor.org/packages/mzID/"
    git      = "https://git.bioconductor.org/packages/mzID.git"

    version('1.14.0', commit='1c53aa6523ae61d3ebb13381381fc119d6cc6115')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
