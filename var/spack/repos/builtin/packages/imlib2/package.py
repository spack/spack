# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Imlib2(AutotoolsPackage):
    """
    Library that does image file loading and saving as well as rendering,
    manipulation, arbitrary polygon support
    """

    homepage = "http://sourceforge.net/projects/enlightenment/"
    url      = "http://downloads.sourceforge.net/enlightenment/imlib2-1.5.1.tar.bz2"

    maintainers = ['TheQueasle']

    version('1.5.1', 'fa4e57452b8843f4a70f70fd435c746ae2ace813250f8c65f977db5d7914baae')

    depends_on('libtiff')
    depends_on('giflib')
    depends_on('bzip2')
    depends_on('freetype')
    depends_on('libxext')
    depends_on('libpng')
    depends_on('libid3tag')
    depends_on('libjpeg-turbo')
