# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ...build_systems.generic import Package


class EcpVizSdk(Package):
    """Package that has a dependency with a variant which
    adds a transitive dependency forced to use non default
    values.
    """

    homepage = "https://dev.null"

    version("1.0")

    depends_on("conditional-constrained-dependencies")
