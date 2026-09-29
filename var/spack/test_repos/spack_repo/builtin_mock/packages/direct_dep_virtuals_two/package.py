# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DirectDepVirtualsTwo(Package):
    version("1.0")
    variant("variant", default=False)
    # Pick netlib-blas as a provider for blas.
    depends_on("blas")
    # Require that netlib-blas is a dependency (and thus the provider of blas).
    requires("%netlib-blas")
