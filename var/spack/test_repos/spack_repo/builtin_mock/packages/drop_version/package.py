# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class DropVersion(Package):
    version("1.3")
    version("1.2")
    version("1.1")
    [drop_version(ver) for ver in ["1.3", "1.1"]]
