# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RR6(RPackage):
    """The R6 package allows the creation of classes with reference semantics,
    similar to R's built-in reference classes. Compared to reference classes,
    R6 classes are simpler and lighter-weight, and they are not built on S4
    classes so they do not require the methods package. These classes allow
    public and private members, and they support inheritance, even when the
    classes are defined in different packages."""

    homepage = "https://github.com/wch/R6/"
    url      = "https://cran.rstudio.com/src/contrib/R6_2.2.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/R6"

    version('2.2.2', '635b58c65bff624a1fab69c6b1989801')
    version('2.2.0', '659d83b2d3f7a308a48332b4cfbdab49')
    version('2.1.2', 'b6afb9430e48707be87638675390e457')

    depends_on('r@3.0:')
