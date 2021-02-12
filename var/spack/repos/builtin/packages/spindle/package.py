# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

    version('0.12', sha256='3fd9d0afefa9072fffdf2cfd80a0b5e557e201a0b0eb02e7379eae65e64eb1f2')
    version('0.11', sha256='ae0b40986a39a42eb2b04930c76023b8c4e8f4835e020d184b0aa114f6597c2f')
    version('0.10', sha256='6974cd3c9e78b300b6a4a78046f3d6f8452923ec0b7e0295477dc96d4b0b1482')
    version('0.9',  sha256='3be459e9465662a8b1e7d22ef6e0bd0f69e67bee711d8aade46d254e057525cc')
    version('0.8.1', sha256='c1e099e913faa8199be5811dc7b8be0266f0d1fd65f0a3a25bb46fbc70954ed6')

    depends_on("launchmon")
