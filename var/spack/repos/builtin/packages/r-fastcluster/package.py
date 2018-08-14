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


class RFastcluster(RPackage):
    """This is a two-in-one package which provides interfaces to both R
       and 'Python'. It implements fast hierarchical, agglomerative
       clustering routines. Part of the functionality is designed as drop-in
       replacement for existing routines: linkage() in the 'SciPy' package
       'scipy.cluster.hierarchy', hclust() in R's 'stats' package, and the
       'flashClust' package. It provides the same functionality with the
       benefit of a much faster implementation. Moreover, there are
       memory-saving routines for clustering of vector data, which go beyond
       what the existing packages provide. For information on how to install
       the 'Python' files, see the file INSTALL in the source distribution."""

    homepage = "http://danifold.net/fastcluster.html"
    url      = "https://cran.r-project.org/src/contrib/fastcluster_1.1.25.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/fastcluster/"

    version('1.1.25', sha256='f3661def975802f3dd3cec5b2a1379f3707eacff945cf448e33aec0da1ed4205')

    depends_on('r@3.0.0:', type=('build', 'run'))
