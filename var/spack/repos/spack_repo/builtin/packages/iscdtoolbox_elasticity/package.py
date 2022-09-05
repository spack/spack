# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IscdtoolboxElasticity(CMakePackage):
    """Elastic is a simple yet efficient finite element solver for linear elasticity problems
    in two and three dimensions."""

    homepage = "https://github.com/ISCDtoolbox"
    url = "https://github.com/ISCDtoolbox/LinearElasticity/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/ISCDtoolbox/LinearElasticity.git"

    license("GPL-3.0-only", checked_by="jcortial-safran")

    maintainers("jcortial-safran")

    version(
        "1.0.0",
        sha256="e25d5cd448f4eb8d15461cea4203e854c87a0504c8343ff01c8f8f55b33ee2b7",
        preferred=True,
    )

    variant("openmp", default=False, description="Enable OpenMP support")

    depends_on("iscdtoolbox_commons +openmp", when="+openmp")
    depends_on("iscdtoolbox_commons ~openmp", when="~openmp")

    patch("user-defined-prefix-path.patch")
