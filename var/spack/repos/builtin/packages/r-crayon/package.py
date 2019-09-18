# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCrayon(RPackage):
    """Colored terminal output on terminals that support 'ANSI' color and
    highlight codes. It also works in 'Emacs' 'ESS'. 'ANSI' color support is
    automatically detected. Colors and highlighting can be combined and nested.
    New styles can also be created easily. This package was inspired by the
    'chalk' 'JavaScript' project."""

    homepage = "https://github.com/r-lib/crayon#readme"
    url      = "https://cloud.r-project.org/src/contrib/crayon_1.3.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/crayon"

    version('1.3.4', '77c7c2906c59a3141306d86c89ffc7d3')
    version('1.3.2', 'fe29c6204d2d6ff4c2f9d107a03d0cb9')
