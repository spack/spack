# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXml(RPackage):
    """Many approaches for both reading and creating XML (and HTML) documents
    (including DTDs), both local and accessible via HTTP or FTP. Also offers
    access to an 'XPath' "interpreter"."""

    homepage = "https://cran.r-project.org/web/packages/XML/index.html"
    url      = "https://cran.r-project.org/src/contrib/XML_3.98-1.9.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/XML"
    version('3.98-1.9', '70dd9d711cf3cbd218eb2b870aee9503')
    version('3.98-1.5', 'd1cfcd56f7aec96a84ffca91aea507ee')
    version('3.98-1.4', '1a7f3ce6f264eeb109bfa57bedb26c14')

    depends_on('libxml2')
