# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RMapplots(RPackage):
    """Data Visualisation on Maps.

    Create simple maps; add sub-plots like pie plots to a map or any other
    plot; format, plot and export gridded data. The package was developed for
    displaying fisheries data but most functions can be used for more generic
    data visualisation."""

    cran = "mapplots"

    version('1.5.1', sha256='37e96d34f37922180e07bb63b4514e07d42eee5bbf0885b278286ee48cf142a3')

    depends_on('r@2.10.0:', type=('build', 'run'))
