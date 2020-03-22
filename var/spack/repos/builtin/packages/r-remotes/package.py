# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRemotes(RPackage):
    """Download and install R packages stored in 'GitHub', 'BitBucket', or
    plain 'subversion' or 'git' repositories. This package provides the
    'install_*' functions in 'devtools'. Indeed most of the code was copied
    over from 'devtools'."""

    homepage = "https://github.com/r-lib/remotes#readme"
    url      = "https://cloud.r-project.org/src/contrib/remotes_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/remotes"

    version('2.1.1', sha256='4e590746fce618094089372b185e1ea234b3337b23c44c44118e942d0fb5118b')

    depends_on('r@3.0.0:', type=('build', 'run'))
