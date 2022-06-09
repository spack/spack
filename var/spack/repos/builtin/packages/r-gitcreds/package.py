# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGitcreds(RPackage):
    """Query 'git' Credentials from 'R'.

    Query, set, delete credentials from the 'git' credential store. Manage
    'GitHub' tokens and other 'git' credentials. This package is to be used by
    other packages that need to authenticate to 'GitHub' and/or other 'git'
    repositories."""

    cran = "gitcreds"

    version('0.1.1', sha256='b14aaf4e910a9d2d6c65c93e645f0b0159c00898e669f917f83c03dfedb1dfea')

    depends_on('git', type='run')
