# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Asciidoc(AutotoolsPackage):
    """A presentable text document format for writing articles, UNIX man
    pages and other small to medium sized documents."""

    homepage = "http://asciidoc.org"
    url      = "http://downloads.sourceforge.net/project/asciidoc/asciidoc/8.6.9/asciidoc-8.6.9.tar.gz"

    version('8.6.9', 'c59018f105be8d022714b826b0be130a')

    depends_on('libxml2')
    depends_on('libxslt')
    depends_on('docbook-xml')
    depends_on('docbook-xsl')
