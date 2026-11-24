# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ConflictVirtual(Package):
    version("1.0")
    variant("conflict_direct", default=False, description="Enable conflict")
    variant("conflict_transitive", default=False, description="Enable conflict")

    depends_on("blas")
    requires("%blas=netlib-blas")

    conflicts("%blas=netlib-blas", when="+conflict_direct")
    conflicts("^blas=netlib-blas", when="+conflict_transitive")
