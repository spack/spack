# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openslide(AutotoolsPackage):
    """OpenSlide reads whole slide image files."""

    homepage = "http://openslide.org/"
    url      = "https://github.com/openslide/openslide/releases/download/v3.4.1/openslide-3.4.1.tar.xz"

    version('3.4.1', 'ad9fa84775ed6b505d6f50bf6420c6bf')

    depends_on('openjpeg')
    depends_on('jpeg')
    depends_on('libtiff')
    depends_on('libxml2')
    depends_on('sqlite@3.6:')
