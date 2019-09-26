# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMlbench(RPackage):
    """A collection of artificial and real-world machine learning benchmark
    problems, including, e.g., several data sets from the UCI repository."""

    homepage = "https://cloud.r-project.org/package=mlbench"
    url      = "https://cloud.r-project.org/src/contrib/mlbench_2.1-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mlbench"

    version('2.1-1', '9f06848b8e137b8a37417c92d8e57f3b')

    depends_on('r@2.10:', type=('build', 'run'))
