# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Freeimage(MakefilePackage):
    """FreeImage is an Open Source library project for developers who would like
       to support popular graphics image formats like PNG, BMP, JPEG, TIFF and
       others as needed by today's multimedia applications"""

    homepage = "http://freeimage.sourceforge.net/"

    version('3.18.0', 'f8ba138a3be233a3eed9c456e42e2578')

    patch('install_fixes.patch', when='@3.18.0')

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/freeimage/Source%20Distribution/{0}/FreeImage{1}.zip"
        return url.format(version, str(version).replace('.', ''))
