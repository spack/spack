# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RRenv(RPackage):
    """Project Environments for R packages.

    A dependency management toolkit for R. Using 'renv', you can create and
    manage project-local R libraries, save the state of these libraries to a
    'lockfile', and later restore your library as required. Together, these
    tools can help make your projects more isolated, portable, and
    reproducible."""

    cran = "renv"

    version('0.15.2', sha256='d07effd329f6d653fec9cb517bc8adf3cd6b711758e439055b6d2f06c88765db')
    version('0.15.1', sha256='36e8c8df4af50f2341053aa567798dfca6852ade10fa70f9dc146fe9f96f9b5b')
    version('0.13.2', sha256='41f208ed957e27c50cbd8b0fff77a434bad963707df85e462419e2edb6719a4a')
