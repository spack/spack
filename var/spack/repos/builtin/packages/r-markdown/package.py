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

    homepage = "https://cran.r-project.org/package=markdown"
    url      = "https://cran.r-project.org/src/contrib/markdown_0.7.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/markdown"

    version('0.8', '5dde829a865ad65bab37a2b9d243b071')
    version('0.7.7', '72deca9c675c7cc9343048edbc29f7ff')

    depends_on('r-mime', type=('build', 'run'))
