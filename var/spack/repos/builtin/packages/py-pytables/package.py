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


class PyPytables(Package):
    """PyTables is a package for managing hierarchical datasets and designed to
    efficiently and easily cope with extremely large amounts of data."""
    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v.3.2.2.tar.gz"

    version('3.2.2', '7cbb0972e4d6580f629996a5bed92441')

    extends('python')
    depends_on('hdf5')
    depends_on('py-numpy', type=nolink)
    depends_on('py-numexpr', type=nolink)
    depends_on('py-cython', type=nolink)
    depends_on('py-setuptools', type='build')

    def install(self, spec, prefix):
        env["HDF5_DIR"] = spec['hdf5'].prefix
        setup_py('install', '--prefix=%s' % prefix)
