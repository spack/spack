# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *

from ..kokkos.package import Kokkos


class Finch(CMakePackage, CudaPackage, ROCmPackage):
    """Heat transfer for additive manufacturing with Cabana"""

    homepage = "https://github.com/ORNL-MDF/Finch"
    git = "https://github.com/ORNL-MDF/Finch.git"
    url = "https://github.com/ORNL-MDF/Finch/archive/0.2.0.tar.gz"

    maintainers("streeve", "MattRolchigo", "colemanjs")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("0.2.0", sha256="cd00fa87be734e800799f47aaa7259d0dbad7110f4c42f6bf59b56c658e2fe60")
    version("0.1.0", sha256="d74612916dcaa8121bac9f0f14b3da665841d82744176c780b3b824503b81430")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")

    depends_on("cxx", type="build")
    depends_on("c", type="build")
    depends_on("cmake@3.12:", type="build")
    depends_on("mpi")
    depends_on("kokkos@3.7:")
    depends_on("cabana+grid+mpi@0.6.1:")
    depends_on("nlohmann-json")

    for _backend in _kokkos_backends:
        # Handled separately below
        if _backend != "cuda" and _backend != "rocm":
            _backend_dep = "+{0}".format(_backend)
            depends_on("kokkos {0}".format(_backend_dep), when=_backend_dep)

    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on("kokkos {0}".format(cuda_dep), when=cuda_dep)
    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("kokkos {0}".format(rocm_dep), when=rocm_dep)

    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
