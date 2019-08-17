# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXml(RPackage):
    """Many approaches for both reading and creating XML (and HTML) documents
    (including DTDs), both local and accessible via HTTP or FTP. Also offers
    access to an 'XPath' "interpreter"."""

    homepage = "https://cloud.r-project.org/package=XML"
    url      = "https://cloud.r-project.org/src/contrib/XML_3.98-1.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/XML"

    version('3.98-1.20', sha256='46af86376ea9a0fb1b440cf0acdf9b89178686a05c4b77728fcff1f023aa4858')
    version('3.98-1.19', sha256='81b1c4a2df24c5747fa8b8ec2d76b4e9c3649b56ca94f6c93fbd106c8a72beab')
    version('3.98-1.9', '70dd9d711cf3cbd218eb2b870aee9503')
    version('3.98-1.5', 'd1cfcd56f7aec96a84ffca91aea507ee')
    version('3.98-1.4', '1a7f3ce6f264eeb109bfa57bedb26c14')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('libxml2@2.6.3:')
