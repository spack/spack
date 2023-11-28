# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


def submodules(package):
    submodules = []
    submodules.append("dakota-examples")
    submodules.append("packages/external")
    submodules.append("packages/pecos")
    submodules.append("packages/surfpack")

    return submodules


class Dakota(CMakePackage):
    """The Dakota toolkit provides a flexible, extensible interface between
    analysis codes and iterative systems analysis methods. Dakota
    contains algorithms for:

    - optimization with gradient and non gradient-based methods;
    - uncertainty quantification with sampling, reliability, stochastic
    - expansion, and epistemic methods;
    - parameter estimation with nonlinear least squares methods;
    - sensitivity/variance analysis with design of experiments and
    - parameter study methods.

    These capabilities may be used on their own or as components within
    advanced strategies such as hybrid optimization, surrogate-based
    optimization, mixed integer nonlinear programming, or optimization
    under uncertainty.

    """

    homepage = "https://dakota.sandia.gov/"
    git = "https://github.com/snl-dakota/dakota.git"
    url = "https://dakota.sandia.gov/sites/default/files/distributions/public/dakota-6.12-release-public.src.tar.gz"

    version(
        "6.18",
        tag="v6.18.0",
        commit="f6cb33b517bb304795e1e14d3673fe289df2ec9b",
        submodules=submodules,
    )
    version("6.12", sha256="4d69f9cbb0c7319384ab9df27643ff6767eb410823930b8fbd56cc9de0885bc9")
    version("6.9", sha256="989b689278964b96496e3058b8ef5c2724d74bcd232f898fe450c51eba7fe0c2")
    version("6.3", sha256="0fbc310105860d77bb5c96de0e8813d75441fca1a5e6dfaf732aa095c4488d52")

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="Activates MPI support")

    # Generic 'lapack' provider won't work, dakota searches for
    # 'LAPACKConfig.cmake' or 'lapack-config.cmake' on the path
    depends_on("netlib-lapack")

    depends_on("blas")
    depends_on("mpi", when="+mpi")

    depends_on("python")
    depends_on("perl-data-dumper", type="build", when="@6.12:")
    depends_on("boost@:1.68.0", when="@:6.12")
    depends_on("boost@1.69.0:", when="@6.18:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@:6.12")
    depends_on("cmake@2.8.9:", type="build")
    depends_on("cmake@3.17:", type="build", when="@6.18:")

    def cmake_args(self):
        spec = self.spec

        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if "+mpi" in spec:
            args.extend(
                [
                    "-DDAKOTA_HAVE_MPI:BOOL=ON",
                    "-DMPI_CXX_COMPILER:STRING=%s" % join_path(spec["mpi"].mpicxx),
                ]
            )

        if self.run_tests:
            args += ["-DCMAKE_CTEST_ARGUMENTS=-L;Accept"]

        return args
