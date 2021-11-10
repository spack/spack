# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRappdirs(RPackage):
    """An easy way to determine which directories on the users computer
    you should use to save data, caches and logs. A port of Python's
    'Appdirs' to R."""

    homepage = "https://cloud.r-project.org/package=rappdirs"
    cran = "rappdirs"

    version('0.3.3', sha256='49959f65b45b0b189a2792d6c1339bef59674ecae92f8c2ed9f26ff9e488c184')
    version('0.3.1', sha256='2fd891ec16d28862f65bb57e4a78f77a597930abb59380e757afd8b6c6d3264a')

    depends_on('r@2.14:', type=('build', 'run'))
    depends_on('r@3.2:', when='@0.3.2:', type=('build', 'run'))
