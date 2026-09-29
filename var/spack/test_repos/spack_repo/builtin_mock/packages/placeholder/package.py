# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Placeholder(Package):
    """Placeholder test package"""

    version("1.5")

    @property
    def fetcher(self):
        msg = "Placeholder package"
        raise InstallError(msg)

    @fetcher.setter
    def fetcher(self, value):
        _ = self.fetcher
