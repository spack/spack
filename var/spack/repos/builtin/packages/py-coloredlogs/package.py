# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColoredlogs(PythonPackage):
    """Colored terminal output for Python's logging module"""

    pypi = "coloredlogs/coloredlogs-10.0.tar.gz"

    version('15.0', sha256='5e78691e2673a8e294499e1832bb13efcfb44a86b92e18109fa18951093218ab')
    version('14.3', sha256='7ef1a7219870c7f02c218a2f2877ce68f2f8e087bb3a55bd6fbaa2a4362b4d52')
    version('14.2', sha256='ac35144b5c39699318fdea8afdf3ca3308f274759af56a479e6d657b1850e246')
    version('14.1', sha256='45add58d9000cae86358f9bb996ffbd788b0cc61df48938dbfc959dbee242f54')
    version('14.0', sha256='a1fab193d2053aa6c0a97608c4342d031f1f93a3d1218432c59322441d31a505')
    version('10.0', sha256='b869a2dda3fa88154b9dd850e27828d8755bfab5a838a1c97fbc850c6e377c36')

    depends_on('py-setuptools', type='build')
    depends_on('py-humanfriendly@4.7:', type=('build', 'run'))
