# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ....builtin_mock.build_systems.generic import Package


class U(Package):
    version("6.0")

    depends_on("y cflags='-e1 -e2'")

    depends_on("c", type="build")
