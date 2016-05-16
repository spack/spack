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

class PyPillow(Package):
    """Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors. The Python Imaging Library (PIL) adds image processing capabilities to your Python interpreter. This library supports many file formats, and provides powerful image processing and graphics capabilities."""

    homepage = "https://python-pillow.github.io/"
    url      = "https://pypi.python.org/packages/source/P/Pillow/Pillow-3.0.0.tar.gz"

    version('3.0.0', 'fc8ac44e93da09678eac7e30c9b7377d')
    provides('PIL')

    # These defaults correspond to Pillow defaults
    variant('jpeg', default=True, description='Provide JPEG functionality')
    variant('zlib', default=True, description='Access to compressed PNGs')
    variant('tiff', default=False, description='Access to TIFF files')
    variant('freetype', default=False, description='Font related services')
    variant('tk', default=False, description='Support for tkinter bitmap and photo images')
    variant('lcms', default=False, description='Color management')

    # Spack does not (yet) support these modes of building
    # variant('webp', default=False, description='')
    # variant('webpmux', default=False, description='')
    # variant('jpeg2000', default=False, description='')

    extends('python')
    depends_on('binutils')
    depends_on('py-setuptools')

    depends_on('jpeg', when='+jpeg')   # BUG: It will use the system libjpeg anyway
    depends_on('zlib', when='+zlib')
    depends_on('tiff', when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms', when='+lcms')
    depends_on('tcl', when='+tk')
    depends_on('tk', when='+tk')

    def install(self, spec, prefix):
        libpath=[]

        if '+jpeg' in spec:
            libpath.append(join_path(spec['jpeg'].prefix, 'lib'))
        if '+zlib' in spec:
            libpath.append(join_path(spec['zlib'].prefix, 'lib'))
        if '+tiff' in spec:
            libpath.append(join_path(spec['tiff'].prefix, 'lib'))
        if '+freetype' in spec:
            libpath.append(join_path(spec['freetype'].prefix, 'lib'))
        if '+lcms' in spec:
            libpath.append(join_path(spec['lcms'].prefix, 'lib'))

        # This has not been tested, and likely needs some other treatment.
        #if '+tk' in spec:
        #    libpath.append(join_path(spec['tcl'].prefix, 'lib'))
        #    libpath.append(join_path(spec['tk'].prefix, 'lib'))

        # -------- Building
        cmd = ['build_ext',
            '--%s-jpeg' % ('enable' if '+jpeg' in spec else 'disable'),
            '--%s-zlib' % ('enable' if '+zlib' in spec else 'disable'),
            '--%s-tiff' % ('enable' if '+tiff' in spec else 'disable'),
            '--%s-freetype' % ('enable' if '+freetype' in spec else 'disable'),
            '--%s-lcms' % ('enable' if '+lcms' in spec else 'disable'),
            '-L'+':'.join(libpath)    # NOTE: This does not make it find libjpeg
            ]

        #if '+tk' in spec:
        #    cmd.extend(['--enable-tcl', '--enable-tk'])
        #else:
        #    cmd.extend(['--disable-tcl', '--disable-tk'])

        # --------- Installation
        cmd.extend(['install', '--prefix=%s' % prefix])

        python('setup.py', *cmd)
