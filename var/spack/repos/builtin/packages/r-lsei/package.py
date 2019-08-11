# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLsei(RPackage):
    """It contains functions that solve least squares linear regression
       problems under linear equality/inequality constraints. Functions for
       solving quadratic programming problems are also available, which
       transform such problems into least squares ones first. It is developed
       based on the 'Fortran' program of Lawson and Hanson (1974, 1995), which
       is public domain and available at
       <http://www.netlib.org/lawson-hanson>."""

    homepage = "https://cloud.r-project.org/package=lsei"
    url      = "https://cloud.r-project.org/src/contrib/lsei_1.2-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lsei"

    version('1.2-0', '18a9322d7a79ecb86b8788645c4b7e3c')
