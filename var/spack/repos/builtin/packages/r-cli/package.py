# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCli(RPackage):
    """A suite of tools designed to build attractive command line interfaces
       ('CLIs'). Includes tools for drawing rules, boxes, trees, and
       'Unicode' symbols with 'ASCII' alternatives."""

    homepage = "https://github.com/r-lib/cli#readme"
    url      = "https://cloud.r-project.org/src/contrib/cli_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/cli"

    version('1.1.0', sha256='4fc00fcdf4fdbdf9b5792faee8c7cf1ed5c4f45b1221d961332cda82dbe60d0a')
    version('1.0.1', 'ef80fbcde15760fd55abbf9413b306e3971b2a7034ab8c415fb52dc0088c5ee4')
    version('1.0.0', 'e6c4169541d394d6d435c4b430b1dd77')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
