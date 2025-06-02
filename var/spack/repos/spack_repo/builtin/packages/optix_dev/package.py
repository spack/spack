# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *


class OptixDev(Package):
    """OptiX is an application framework for achieving optimal ray tracing
    performance on the GPU. This package contains the minimal set of necessary
    header files for building an application with OptiX support, including
    access to the OptiX functions provided by the NVIDIA display driver.
    https://github.com/NVIDIA/optix-dev It is not necessary to use this
    package when installing the complete OptiX SDK; header files are already
    included in the OptiX SDK."""

    homepage = "https://developer.nvidia.com/rtx/ray-tracing/optix"
    url = "https://github.com/NVIDIA/optix-dev/archive/refs/tags/v9.0.0.tar.gz"

    license("LicenseRef-NvidiaProprietary AND BSD-3-Clause")

    maintainers("plexoos")
    build_system("generic")

    version("9.0.0", sha256="069a5860040ea611e7eb6317f8e3bb0f0d54a5acac744568f7290d7cb8711c05")
    version("8.1.0", sha256="aa32dfb55f37ff92964a5545b056094d86635441b3513e1d45a9410404b6d7c2")
    version("8.0.0", sha256="b32e74c9f5c13549ff3a9760076271b5b6ec28f93fe6a8dd0bde74d7e5c58e05")
    version("7.7.0", sha256="02e5acdb8870a5668c763d47043d61586c1c4e72395d64e7bdd99ea04bc4222d")
    version("7.6.0", sha256="4fe1e047d0e80980e57c469e3491f88cd3c3b735462b35cb3a0c2797a751fb1e")
    version("7.5.0", sha256="9053ba3636dd612ad5e50106a56ea4022e719a2d35c914c61fc9bc681b0e64d6")
    version("7.4.0", sha256="91d35f1ba0f519f9e98582586478a64d323e7d7263b8b8349797c4aeb7fc53af")
    version("7.3.0", sha256="a74b0120e308258f5b5d5b30f905e13e1ceeeca2058aaee58310c84647fcc31d")
    version("7.2.0", sha256="a82bc7da75f3db81be73826a00b694c858be356258323d454f4e1aa78a5670f8")
    version("7.1.0", sha256="70b9adac04e5a36185e715a74306f22426334b6a3850dd7f1a2744212c83f9e1")
    version("7.0.0", sha256="8b294bcd4d23ced20310d73ed320c7bc3ecbb79e3d50f00eb5d97a3639d129a3")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
        install("LICENSE.txt", prefix)
        install("license_info.txt", prefix)
