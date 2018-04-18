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


class PyLineProfiler(PythonPackage):
    """Line-by-line profiler."""

    homepage = "https://github.com/rkern/line_profiler"
    url      = "https://pypi.io/packages/source/l/line_profiler/line_profiler-2.0.tar.gz"

    version('2.0', 'fc93c6bcfac3b7cb1912cb28836d7ee6')

    depends_on('python@2.5:')
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython',         type='build')
    depends_on('py-ipython@0.13:',  type=('build', 'run'))
