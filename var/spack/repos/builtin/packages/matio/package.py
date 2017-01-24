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


class Matio(AutotoolsPackage):
    """matio is an C library for reading and writing Matlab MAT files"""
    homepage = "http://sourceforge.net/projects/matio/"
    url = "http://downloads.sourceforge.net/project/matio/matio/1.5.9/matio-1.5.9.tar.gz"

    version('1.5.9', 'aab5b4219a3c0262afe7eeb7bdd2f463')
    version('1.5.2', '85b007b99916c63791f28398f6a4c6f1')

    variant("zlib", default=True,
            description='support for compressed mat files')
    variant("hdf5", default=True,
            description='support for version 7.3 mat files via hdf5')
    variant("shared", default=True, description='Enables the build of shared libraries.')


    depends_on("zlib", when="+zlib")
    depends_on("hdf5", when="+hdf5")

    def configure_args(self):
        args = []
        if '+zlib' in self.spec:
            args.append("--with-zlib=%s" % self.spec['zlib'].prefix)
        if '+hdf5' in self.spec:
            args.append("--with-hdf5=%s" % self.spec['hdf5'].prefix)
        if '+shared' not in self.spec:
            args.append("--disable-shared")
        return args
