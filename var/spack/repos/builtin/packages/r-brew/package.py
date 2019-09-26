# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBrew(RPackage):
    """brew implements a templating framework for mixing text and R code for
    report generation. brew template syntax is similar to PHP, Ruby's erb
    module, Java Server Pages, and Python's psp module."""

    homepage = "https://cloud.r-project.org/package=brew"
    url      = "https://cloud.r-project.org/src/contrib/brew_1.0-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/brew"

    version('1.0-6', '4aaca5e6ec145e0fc0fe6375ce1f3806')
