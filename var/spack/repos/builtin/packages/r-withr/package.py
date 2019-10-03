# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RWithr(RPackage):
    """A set of functions to run code 'with' safely and temporarily modified
    global state. Many of these functions were originally a part of the
    'devtools' package, this provides a simple package with limited
    dependencies to provide access to these functions."""

    homepage = "http://github.com/jimhester/withr"
    url      = "https://cloud.r-project.org/src/contrib/withr_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/withr"

    version('2.1.2', sha256='41366f777d8adb83d0bdbac1392a1ab118b36217ca648d3bb9db763aa7ff4686')
    version('1.0.2', 'ca52b729af9bbaa14fc8b7bafe38663c')
    version('1.0.1', 'ac38af2c6f74027c9592dd8f0acb7598')

    depends_on('r@3.0.2:', type=('build', 'run'))
