##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class GtkDoc(AutotoolsPackage):
    """GTK-Doc is a project which was started to
    generate API documentation from comments added to C code."""

    homepage = "https://www.gtk.org/gtk-doc/"
    url      = "https://download.gnome.org/sources/gtk-doc/1.27/gtk-doc-1.27.tar.xz"

    version('1.27', 'b29949e0964762e474b706ce22171602')

    depends_on('python')
    depends_on('py-six')
    depends_on('libxslt')
    depends_on('libxml2')
    depends_on('docbook-xml@4.3')
    depends_on('docbook-xsl')

    def configure_args(self):
        spec = self.spec
        return ['--with-xml-catalog=%s/catalog.xml' % spec['docbook-xml'].prefix]
