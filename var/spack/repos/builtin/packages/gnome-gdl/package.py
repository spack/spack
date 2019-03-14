# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GnomeGdl(AutotoolsPackage):
    """Gnome Docking library. Provides docking features for gtk+."""

    homepage = "https://github.com/GNOME/gdl"
    url      = "https://ftp.gnome.org/pub/gnome/sources/gdl/3.28/gdl-3.28.0.tar.xz"

    version('3.28.0', sha256='52cc98ecc105148467b3b2b4e0d27ae484b1b6710d53413f771ed07ef1b737b6')

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('libxml2@2.2.8:')
    depends_on('gtkplus@3:')

    def configure_args(self):
        args = ['--enable-static']
        return args
