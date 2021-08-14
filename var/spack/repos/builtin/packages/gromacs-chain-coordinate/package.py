# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack.pkg.builtin.gromacs import Gromacs as BuiltinGromacs


def filter_versions(version_list, allowed_names):
    return dict((key, value) for key, value in version_list.items() if str(key) in allowed_names)


class GromacsChainCoordinate(BuiltinGromacs):
    """
    A modification of GROMACS that implements the "chain coordinate", a reaction
    coordinate for pore formation in membranes and stalk formation between membranes.
    """

    homepage = 'https://gitlab.com/cbjh/gromacs-chain-coordinate/-/blob/main/README.md'
    url = 'https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.1/gromacs-chain-coordinate-release-2021.chaincoord-0.1.tar.bz2'
    git = 'https://gitlab.com/cbjh/gromacs-chain-coordinate.git'
    maintainers = ['w8jcik']

    version('main', branch='main')
    version('2021.2-0.1', sha256="879fdd04662370a76408b72c9fbc4aff60a6387b459322ac2700d27359d0dd87",
            url="https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.1/gromacs-chain-coordinate-release-2021.chaincoord-0.1.tar.bz2", preferred=True)

    def __init__(self, spec):
        super().__init__(spec)

        self.versions = filter_versions(self.versions, ['main', '2021.2-0.1'])
