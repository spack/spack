# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Spindle(AutotoolsPackage):
    """Spindle improves the library-loading performance of dynamically
       linked HPC applications.  Without Spindle large MPI jobs can
       overload on a shared file system when loading dynamically
       linked libraries, causing site-wide performance problems.
    """
    homepage = "https://computing.llnl.gov/project/spindle/"
    url      = "https://github.com/hpc/Spindle/archive/v0.8.1.tar.gz"

    version('0.8.1', 'f11793a6b9d8df2cd231fccb2857d912')

    depends_on("launchmon")
