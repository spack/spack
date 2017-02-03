##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class PyPypar(PythonPackage):
    """Pypar is an efficient but easy-to-use module that allows programs
       written in Python to run in parallel on multiple processors and
       communicate using MPI."""
    homepage = "http://code.google.com/p/pypar/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-2.1.5_108.tgz"

    version('2.1.5_108', '7a1f28327d2a3b679f9455c843d850b8')

    depends_on('mpi')
    depends_on('py-numpy', type=('build', 'run'))

    build_directory = 'source'

    def url_for_version(self, version):
        return "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-%s.tgz" % version
