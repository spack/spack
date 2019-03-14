# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Inkscape(CMakePackage):
    """Inkscape is professional quality vector graphics software which runs on
    Windows, Mac OS X and GNU/Linux. It is used by design professionals and
    hobbyists worldwide, for creating a wide variety of graphics such as
    illustrations, icons, logos, diagrams, maps and web graphics. Inkscape uses
    the W3C open standard SVG (Scalable Vector Graphics) as its native format,
    and is free and open-source software."""

    homepage = "https://inkscape.org/"

    version('0.92.3', sha256='063296c05a65d7a92a0f627485b66221487acfc64a24f712eb5237c4bd7816b2',
            url="https://inkscape.org/gallery/item/12187/inkscape-0.92.3.tar.bz2")

    variant('gtk3', default=False, description='Enable experimental Gtk+ 3 build')

    # http://wiki.inkscape.org/wiki/index.php/Tracking_Dependencies
    depends_on('cmake@2.8.2:', type='build')
    depends_on('bdw-gc@7.2:')  # Boehm-GC
    depends_on('cairo@1.10:')
    depends_on('gnome-gdl@3.4:', when='+gtk3')  # GDL
    depends_on('glib@2.28:')
    depends_on('gtkplus@2.24:2.999', when='~gtk3')
    depends_on('gtkplus@3.8:', when='+gtk3')
    depends_on('gsl')
    depends_on('lcms@1.13:')
    # depends_on('libxml2@2.6.11:')
    # depends_on('libxslt@1.0.15:')
    depends_on('pango@1.24:')
    depends_on('poppler@0.20.0:')
    # depends_on('libsigcpp@2.0.12:')

    def cmake_args(self):
        args = []
        return args
