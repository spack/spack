# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *

from ...build_systems.generic import Package


class V1Provider(Package):
    """Mimic the real netlib-lapack, that may be built on top of an
    optimized blas.
    """

    homepage = "https://dev.null"

    version("1.0")

    provides("v1")
