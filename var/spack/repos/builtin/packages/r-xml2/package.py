# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RXml2(RPackage):
    """Work with XML files using a simple, consistent interface. Built on top
       of the 'libxml2' C library."""

    homepage = "https://cloud.r-project.org/package=xml2"
    url      = "https://cloud.r-project.org/src/contrib/xml2_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xml2"

    version('1.2.2', sha256='3050f147c4335be2925a576557bbda36bd52a5bba3110d47b740a2dd811a78f4')
    version('1.2.1', sha256='5615bbc94607efc3bc192551992b349091df802ae34b855cfa817733f2690605')
    version('1.1.1', '768f7edc39c4baab6b6b9e7c7ec79fee')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.12:', type=('build', 'run'))
    depends_on('r-bh', when='@:1.1.1', type=('build', 'run'))
    depends_on('libxml2')
