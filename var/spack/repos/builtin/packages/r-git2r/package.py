# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGit2r(RPackage):
    """Interface to the 'libgit2' library, which is a pure C implementation of
    the 'Git' core methods. Provides access to 'Git' repositories to extract
    data and running some basic 'Git' commands."""

    homepage = "https://github.com/ropensci/git2r"
    url      = "https://cran.r-project.org/src/contrib/git2r_0.18.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/git2r"

    version('0.18.0', 'fb5741eb490c3d6e23a751a72336f24d')
    version('0.15.0', '57658b3298f9b9aadc0dd77b4ef6a1e1')

    depends_on('r@3.0.2:')

    depends_on('zlib')
    depends_on('openssl')
