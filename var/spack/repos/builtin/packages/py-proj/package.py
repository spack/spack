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


class PyProj(PythonPackage):
    """Python interface to the PROJ.4 Library."""
    homepage = "http://jswhit.github.io/pyproj/"
    url      = "https://github.com/jswhit/pyproj/tarball/v1.9.5.1rel"

    # This is not a tagged release of pyproj.
    # The changes in this "version" fix some bugs, especially with Python3 use.
    version('1.9.5.1.1', 'd035e4bc704d136db79b43ab371b27d2',
        url='https://www.github.com/jswhit/pyproj/tarball/0be612cc9f972e38b50a90c946a9b353e2ab140f')

    version('1.9.5.1', 'a4b80d7170fc82aee363d7f980279835')

    depends_on('py-cython', type='build')
    depends_on('py-setuptools', type='build')

    # NOTE: py-proj does NOT depends_on('proj').
    # The py-proj git repo actually includes the correct version of PROJ.4,
    # which is built internally as part of the py-proj build.
    # Adding depends_on('proj') will cause mysterious build errors.
