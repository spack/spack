# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMarkdown(RPackage):
    """Provides R bindings to the 'Sundown' 'Markdown' rendering library
    (https://github.com/vmg/sundown). 'Markdown' is a plain-text formatting
    syntax that can be converted to 'XHTML' or other formats. See
    http://en.wikipedia.org/wiki/Markdown for more information about
    'Markdown'."""

    homepage = "https://cloud.r-project.org/package=markdown"
    url      = "https://cloud.r-project.org/src/contrib/markdown_0.7.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/markdown"

    version('1.1', sha256='8d8cd47472a37362e615dbb8865c3780d7b7db694d59050e19312f126e5efc1b')
    version('1.0', sha256='172d8072d1829644ee6cdf54282a55718e2cfe9c9915d3589ca5f9a016f8d9a6')
    version('0.9', sha256='3068c6a41ca7a76cbedeb93b7371798f4d8437eea69a23c0ed5204c716d1bf23')
    version('0.8', '5dde829a865ad65bab37a2b9d243b071')
    version('0.7.7', '72deca9c675c7cc9343048edbc29f7ff')

    depends_on('r@2.11.1:', type=('build', 'run'))
    depends_on('r-mime@0.3:', type=('build', 'run'))
    depends_on('r-xfun', when='@1.1:', type=('build', 'run'))
