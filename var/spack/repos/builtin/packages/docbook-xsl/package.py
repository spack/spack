# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class DocbookXsl(Package):
    """DocBook XSLT 1.0 Stylesheets."""

    homepage = "https://github.com/docbook/xslt10-stylesheets"
    url      = "https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F1.79.2/docbook-xsl-1.79.2.tar.bz2"

    version('1.79.2', sha256='316524ea444e53208a2fb90eeb676af755da96e1417835ba5f5eb719c81fa371')

    depends_on('docbook-xml')

    patch('docbook-xsl-1.79.2-stack_fix-1.patch', when='@1.79.2')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def setup_environment(self, spack_env, run_env):
        catalog = os.path.join(self.prefix, 'catalog.xml')
        run_env.set('XML_CATALOG_FILES', catalog, separator=' ')
