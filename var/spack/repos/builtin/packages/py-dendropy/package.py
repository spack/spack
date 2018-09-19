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


class PyDendropy(PythonPackage):
    """DendroPy is a Python library for phylogenetic computing. It provides
    classes and functions for the simulation, processing, and manipulation of
    phylogenetic trees and character matrices, and supports the reading and
    writing of phylogenetic data in a range of formats, such as NEXUS, NEWICK,
    NeXML, Phylip, FASTA, etc."""

    homepage = "https://www.dendropy.org"
    url      = "https://pypi.io/packages/source/d/dendropy/DendroPy-4.3.0.tar.gz"

    version('4.3.0',  '56c37eb7db69686c8ef3467562f4e7c5')
    version('3.12.0', '6971ac9a8508b4198fd357fab0affc84')

    depends_on('python@2.7:,3.4:')
    depends_on('py-setuptools', type='build')
