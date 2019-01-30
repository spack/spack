# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class DocbookXsl(Package):
    """Docbook XSL vocabulary."""
    homepage = "http://docbook.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/docbook/docbook-xsl/1.79.1/docbook-xsl-1.79.1.tar.bz2"

    version('1.79.1', 'b48cbf929a2ad85e6672f710777ca7bc')

    depends_on('docbook-xml')

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
