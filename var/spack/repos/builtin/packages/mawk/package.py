# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mawk(AutotoolsPackage):
    """mawk is an interpreter for the AWK Programming Language."""

    homepage = "http://invisible-island.net/mawk/mawk.html"
    url      = "http://invisible-mirror.net/archives/mawk/mawk-1.3.4.tgz"

    version('1.3.4-20171017', sha256='db17115d1ed18ed1607c8b93291db9ccd4fe5e0f30d2928c3c5d127b23ec9e5b')
    version('1.3.4', 'b1d27324ae80302452d0fa0c98447b65')

    provides('awk')
