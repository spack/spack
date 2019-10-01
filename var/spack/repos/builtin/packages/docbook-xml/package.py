# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class DocbookXml(Package):
    """Docbook DTD XML files."""

    homepage = "https://www.oasis-open.org/docbook"
    url      = "https://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"
    list_url = "https://www.oasis-open.org/docbook/xml/"
    list_depth = 1

    version('4.5', '03083e288e87a7e829e437358da7ef9e')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        catalog = os.path.join(self.prefix, 'catalog.xml')
        run_env.set('XML_CATALOG_FILES', catalog, separator=' ')
