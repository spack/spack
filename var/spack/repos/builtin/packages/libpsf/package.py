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
import os


class Libpsf(Package):
    """libpsf is a c++ library that reads Cadence PSF waveform files"""

    homepage = "https://github.com/henjo/libpsf"

    version('master', git='https://github.com/henjo/libpsf.git', branch='master')

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool",  type="build")

    variant('python', default=True, description='Build python wrappers')
    extends('python',                         when='+python')
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('boost+python',                when='+python')
    depends_on('py-numpy',                    when='+python')

    patch('fix_link.patch', level=0)
    patch('fix_install.patch', level=0)

    def install(self, spec, prefix):
        autoreconf = which("autoreconf")
        libtoolize()
        autoreconf('--force', '--install', '--verbose', '-Im4')
        if '+python' in spec:
            configure("--prefix=%s" % prefix, '--with-python')
        else:
            configure("--prefix=%s" % prefix)
        make()
        # FIXME: Add logic to build and install here.
        # FIXME: Add logic to build and install here.
        make("install")
