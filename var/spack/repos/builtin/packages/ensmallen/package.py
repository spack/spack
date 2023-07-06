# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ensmallen(CMakePackage):
    """ensmallen is a high-quality C++ library for non-linear numerical
    optimization.

    ensmallen provides many types of optimizers that can be used for
    virtually any numerical optimization task. This includes gradient
    descent techniques, gradient-free optimizers, and constrained
    optimization. ensmallen also allows optional callbacks to customize
    the optimization process."""

    homepage = "https://ensmallen.org"
    url = "https://github.com/mlpack/ensmallen/archive/refs/tags/2.19.1.tar.gz"

    version("2.19.1", sha256="f36ad7f08b0688d2a8152e1c73dd437c56ed7a5af5facf65db6ffd977b275b2e")

    variant("openmp", default=True, description="Use OpenMP for parallelization")

    depends_on("cmake@3.3.2:")
    depends_on("armadillo@9.800.0:")

    def cmake_args(self):
        args = [self.define_from_variant("USE_OPENMP", "openmp")]
        return args
