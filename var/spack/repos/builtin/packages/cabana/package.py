# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos


class Cabana(CMakePackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit"""

    homepage = "https://github.com/ECP-copa/Cabana"
    git = "https://github.com/ECP-copa/Cabana.git"
    url = "https://github.com/ECP-copa/Cabana/archive/0.5.0.tar.gz"

    maintainers("junghans", "streeve", "sslattery")

    tags = ["e4s", "ecp"]

    version("master", branch="master")
    version("0.5.0", sha256="b7579d44e106d764d82b0539285385d28f7bbb911a572efd05c711b28b85d8b1")
    version("0.4.0", sha256="c347d23dc4a5204f9cc5906ccf3454f0b0b1612351bbe0d1c58b14cddde81e85")
    version("0.3.0", sha256="fb67ab9aaf254b103ae0eb5cc913ddae3bf3cd0cf6010e9686e577a2981ca84f")
    version("0.2.0", sha256="3e0c0e224e90f4997f6c7e2b92f00ffa18f8bcff72f789e0908cea0828afc2cb")
    version("0.1.0", sha256="3280712facf6932b9d1aff375b24c932abb9f60a8addb0c0a1950afd0cb9b9cf")
    version("0.1.0-rc0", sha256="73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")
    variant("mpi", default=True, description="Build with mpi support")
    variant("arborx", default=False, description="Build with ArborX support")
    variant("heffte", default=False, description="Build with heFFTe support")
    variant("hypre", default=False, description="Build with HYPRE support")
    variant("cajita", default=False, description="Build Cajita subpackage")
    variant("testing", default=False, description="Build unit tests")
    variant("examples", default=False, description="Build tutorial examples")
    variant("performance_testing", default=False, description="Build performance tests")

    depends_on("cmake@3.9:", type="build", when="@:0.4.0")
    depends_on("cmake@3.16:", type="build", when="@0.5.0:")
    depends_on("googletest", type="build", when="testing")
    _versions = {":0.2": "-legacy", "0.3:": "@3.1:", "0.4:": "@3.2:", "master": "@3.4:"}
    for _version in _versions:
        _kk_version = _versions[_version]
        for _backend in _kokkos_backends:
            if _kk_version == "-legacy" and _backend == "pthread":
                _kk_spec = "kokkos-legacy+pthreads"
            elif _kk_version == "-legacy" and _backend not in ["serial", "openmp", "cuda"]:
                continue
            else:
                _kk_spec = "kokkos{0}+{1}".format(_kk_version, _backend)
            depends_on(_kk_spec, when="@{0}+{1}".format(_version, _backend))
    depends_on("arborx", when="@0.3.0:+arborx")
    depends_on("hypre-cmake@2.22.0:", when="@0.4.0:+hypre")
    depends_on("hypre-cmake@2.22.1:", when="@0.5.0:+hypre")
    # Heffte pinned at 2.x.0 because its cmakefiles can't roll forward
    # compatibilty to later minor versions.
    depends_on("heffte@2.0.0", when="@0.4.0+heffte")
    depends_on("heffte@2.1.0", when="@0.5.0:+heffte")
    depends_on("mpi", when="+mpi")

    conflicts("+cajita ~mpi")

    conflicts("+rocm", when="@:0.2.0")
    conflicts("+sycl", when="@:0.3.0")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        enable = ["CAJITA", "TESTING", "EXAMPLES", "PERFORMANCE_TESTING"]
        require = ["ARBORX", "HEFFTE", "HYPRE"]

        # These variables were removed in 0.3.0 (where backends are
        # automatically used from Kokkos)
        if self.spec.satisfies("@:0.2.0"):
            enable += ["Serial", "OpenMP", "Cuda"]
        # MPI was changed from ENABLE to REQUIRE in 0.4.0
        if self.spec.satisfies("@:0.3.0"):
            enable += ["MPI"]
        else:
            require += ["MPI"]

        for category, cname in zip([enable, require], ["ENABLE", "REQUIRE"]):
            for var in category:
                cbn_option = "Cabana_{0}_{1}".format(cname, var)
                options.append(self.define_from_variant(cbn_option, var.lower()))

        return options
