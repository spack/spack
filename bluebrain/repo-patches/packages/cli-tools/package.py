# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CliTools(BundlePackage):
    """Meta package to bundle python packages for development"""

    version('0.1')

    homepage = "http://www.dummy.org/"
    url      = "https://www.dummy.org/source/dummy-0.2.zip"

    depends_on('byobu', type=('build', 'run'))
    depends_on('tmux', type=('build', 'run'))
