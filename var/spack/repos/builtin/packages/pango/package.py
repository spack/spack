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


class Pango(Package):
    """Pango is a library for laying out and rendering of text, with
       an emphasis on internationalization. It can be used anywhere
       that text layout is needed, though most of the work on Pango so
       far has been done in the context of the GTK+ widget toolkit."""
    homepage = "http://www.pango.org"
    url      = "http://ftp.gnome.org/pub/gnome/sources/pango/1.36/pango-1.36.8.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/pango/"
    list_depth = 2

    version('1.36.8', '217a9a753006275215fa9fa127760ece')
    version('1.40.1', '6fc88c6529890d6c8e03074d57a3eceb')

    depends_on("pkg-config", type="build")
    depends_on("harfbuzz")
    depends_on("cairo")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install", parallel=False)
