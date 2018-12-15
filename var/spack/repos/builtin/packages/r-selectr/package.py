# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSelectr(RPackage):
    """Translates a CSS3 selector into an equivalent XPath expression. This
       allows us to use CSS selectors when working with the XML package as it
       can only evaluate XPath expressions. Also provided are convenience
       functions useful for using CSS selectors on XML nodes. This package
       is a port of the Python package 'cssselect'
       (<https://pythonhosted.org/cssselect/>)."""

    homepage = "https://sjp.co.nz/projects/selectr"
    url      = "https://cran.r-project.org/src/contrib/selectr_0.3-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/selectr"

    version('0.3-1', '7190fcdea1823ad7ef429cab6938e960')

    depends_on('r-testthat', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-xml2', type=('build', 'run'))
