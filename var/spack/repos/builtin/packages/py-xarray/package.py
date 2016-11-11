##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
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


class PyXarray(Package):

    """xarray (formerly xray) is an open source project and Python package
    that aims to bring the labeled data power of pandas to the
    physical sciences, by providing N-dimensional variants of the core
    pandas data structures.
    """

    homepage = "http://xarray.pydata.org"
    url = "https://github.com/pydata/xarray/tarball/v0.8.2"

    version('0.8.2', '393fe6a66f61180e48e736e1cc77be73')

    extends('python')
    depends_on('py-pandas@0.15.0:', type=nolink)
    depends_on('py-numpy@1.7:', type=nolink)

    def install(self, spec, prefix):
        setup_py('install', '--prefix={0}'.format(prefix))
