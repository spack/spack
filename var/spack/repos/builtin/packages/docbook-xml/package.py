# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    def setup_environment(self, spack_env, run_env):
        catalog = os.path.join(self.spec.prefix, 'catalog.xml')
        run_env.set('XML_CATALOG_FILES', catalog, separator=' ')
