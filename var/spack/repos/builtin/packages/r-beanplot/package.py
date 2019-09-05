# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBeanplot(RPackage):
    """Plots univariate comparison graphs, an alternative to
       boxplot/stripchart/violin plot."""

    homepage = "https://cloud.r-project.org/package=beanplot"
    url      = "https://cloud.r-project.org/src/contrib/beanplot_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/beanplot"

    version('1.2', 'b24943208a4e61ee9ee0dc152634d5da')
