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


class PyImageio(PythonPackage):
    """ Imageio is a Python library that provides an easy interface
    to read and write a wide range of image data, including animated
    images, video, volumetric data, and scientific formats. It is
    cross-platform, runs on Python 2.7 and 3.4+, and is easy to install."""

    homepage = "http://imageio.github.io/"
    url      = "https://pypi.io/packages/source/i/imageio/imageio-2.3.0.tar.gz"

    version('2.3.0', '4722c4e1c366748abcb18729881cffb8')

    # TODO: Add variants for plugins, and optional dependencies

    # Fix for python 2 if needed.
    depends_on('py-numpy',            type=('build', 'run'))
    depends_on('py-pillow',           type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',       type='build')
    depends_on('ffmpeg',              type='run')
