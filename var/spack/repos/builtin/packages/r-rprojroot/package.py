# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRprojroot(RPackage):
    """Robust, reliable and flexible paths to files below a project root.
    The 'root' of a project is defined as a directory that matches a
    certain criterion, e.g., it contains a certain regular file."""

    homepage = "https://cloud.r-project.org/package=rprojroot"
    url      = "https://cloud.r-project.org/src/contrib/rprojroot_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rprojroot"

    version('1.3-2', sha256='df5665834941d8b0e377a8810a04f98552201678300f168de5f58a587b73238b')
    version('1.2', 'c1a0574aaac2a43a72f804abbaea19c3')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-backports', type=('build', 'run'))
