# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RROo(RPackage):
    """Methods and classes for object-oriented programming in R with
    or without references. Large effort has been made on making
    definition of methods as simple as possible with a minimum of
    maintenance for package developers. The package has been developed
    since 2001 and is now considered very stable. This is a
    cross-platform package implemented in pure R that defines
    standard S3 classes without any tricks."""

    homepage = "https://github.com/HenrikBengtsson/R.oo"
    url      = "https://cloud.r-project.org/src/contrib/R.oo_1.21.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/R.oo"

    version('1.22.0', sha256='c0862e4608fb2b8f91ec4494d46c2f3ba7bc44999f9aa3d7b9625d3792e7dd4c')
    version('1.21.0', 'f0062095c763faaeba30558303f68bc3')

    depends_on('r@2.13.0:', type=('build', 'run'))
    depends_on('r-r-methodss3@1.7.1:', type=('build', 'run'))
