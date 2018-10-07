# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RArgparse(RPackage):
    """A command line parser to be used with Rscript to write "#!"
       shebang scripts that gracefully accept positional and optional
       arguments and automatically generate usage."""

    homepage = "https://github.com/trevorld/argparse"
    url      = "https://cran.r-project.org/src/contrib/argparse_1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/argparse"

    version('1.1.1', sha256='441449f0816411a868fd1b15cf4b2bc45931bbd4b67d6592dbe48875905cf93b')

    depends_on('r-proto@1:', type=('build', 'run'))
    depends_on('r-findpython', type=('build', 'run'))
    depends_on('r-getopt@1.19', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
