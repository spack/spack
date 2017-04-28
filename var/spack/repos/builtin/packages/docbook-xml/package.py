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
import os
from spack import *


class DocbookXml(Package):
    """Docbook DTD XML files."""
    homepage = "http://www.oasis-open.org/docbook"
    url = "http://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"

    version('4.5', '03083e288e87a7e829e437358da7ef9e')

    def install(self, spec, prefix):
        for item in os.listdir('.'):
            src = os.path.abspath(item)
            dst = os.path.join(prefix, item)
            if os.path.isdir(item):
                install_tree(src, dst, symlinks=True)
            else:
                install(src, dst)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        catalog = os.path.join(self.spec.prefix, 'catalog.xml')
        spack_env.set('XML_CATALOG_FILES', catalog, separator=' ')

    def setup_environment(self, spack_env, run_env):
        catalog = os.path.join(self.spec.prefix, 'catalog.xml')
        run_env.set('XML_CATALOG_FILES', catalog, separator=' ')
