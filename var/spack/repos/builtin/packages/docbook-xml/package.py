# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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

    version('4.5', sha256='4e4e037a2b83c98c6c94818390d4bdd3f6e10f6ec62dd79188594e26190dc7b4')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_run_environment(self, env):
        catalog = os.path.join(self.prefix, 'catalog.xml')
        env.set('XML_CATALOG_FILES', catalog, separator=' ')
