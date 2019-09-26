# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPlogr(RPackage):
    """A simple header-only logging library for C++. Add
    'LinkingTo: plogr' to 'DESCRIPTION', and '#include <plogr.h>'
    in your C++ modules to use it."""

    homepage = "https://cloud.r-project.org/package=plogr"
    url      = "https://cloud.r-project.org/src/contrib/plogr_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plogr"

    version('0.2.0', sha256='0e63ba2e1f624005fe25c67cdd403636a912e063d682eca07f2f1d65e9870d29')
    version('0.1-1', '5ee46ed21b5c571d02900219098517c0')
