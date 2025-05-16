# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from spack_repo.builtin_mock.build_systems.generic import Package


class Y(Package):
    version("2.1")
    version("2.0")

    depends_on("c", type="build")
