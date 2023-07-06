# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class KokkosNvccWrapper(Package):
    """The NVCC wrapper provides a wrapper around NVCC to make it a
    'full' C++ compiler that accepts all flags"""

    # We no longer maintain this as a separate repo
    # Download the Kokkos repo and install from there
    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/archive/3.1.01.tar.gz"

    maintainers("Rombur")

    version("4.0.01", sha256="bb942de8afdd519fd6d5d3974706bfc22b6585a62dd565c12e53bdb82cd154f0")
    version("4.0.00", sha256="1829a423883d4b44223c7c3a53d3c51671145aad57d7d23e6a1a4bebf710dcf6")
    version("3.7.02", sha256="5024979f06bc8da2fb696252a66297f3e0e67098595a0cc7345312b3b4aa0f54")
    version("3.7.01", sha256="0481b24893d1bcc808ec68af1d56ef09b82a1138a1226d6be27c3b3c3da65ceb")
    version("3.7.00", sha256="62e3f9f51c798998f6493ed36463f66e49723966286ef70a9dcba329b8443040")
    version("3.6.01", sha256="1b80a70c5d641da9fefbbb652e857d7c7a76a0ebad1f477c253853e209deb8db")
    version("3.6.00", sha256="53b11fffb53c5d48da5418893ac7bc814ca2fde9c86074bdfeaa967598c918f4")
    version("3.5.00", sha256="748f06aed63b1e77e3653cd2f896ef0d2c64cb2e2d896d9e5a57fec3ff0244ff")
    version("3.4.01", sha256="146d5e233228e75ef59ca497e8f5872d9b272cb93e8e9cdfe05ad34a23f483d1")
    version("3.4.00", sha256="2e4438f9e4767442d8a55e65d000cc9cde92277d415ab4913a96cd3ad901d317")
    version("3.3.01", sha256="4919b00bb7b6eb80f6c335a32f98ebe262229d82e72d3bae6dd91aaf3d234c37")
    version("3.3.00", sha256="170b9deaa1943185e928f8fcb812cd4593a07ed7d220607467e8f0419e147295")
    version("3.2.01", sha256="9e27a3d8f81559845e190d60f277d84d6f558412a3df3301d9545e91373bcaf1")
    version("3.2.00", sha256="05e1b4dd1ef383ca56fe577913e1ff31614764e65de6d6f2a163b2bddb60b3e9")
    version("3.1.01", sha256="ff5024ebe8570887d00246e2793667e0d796b08c77a8227fe271127d36eec9dd")
    version("3.1.00", sha256="b935c9b780e7330bcb80809992caa2b66fd387e3a1c261c955d622dae857d878")
    version("3.0.00", sha256="c00613d0194a4fbd0726719bbed8b0404ed06275f310189b3493f5739042a92b")
    version("master", branch="master")
    version("develop", branch="develop")

    depends_on("cuda")

    def install(self, spec, prefix):
        src = os.path.join("bin", "nvcc_wrapper")
        mkdir(prefix.bin)
        install(src, prefix.bin)

    def setup_dependent_build_environment(self, env, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        env.set("CUDA_ROOT", dependent_spec["cuda"].prefix)
        env.set("NVCC_WRAPPER_DEFAULT_COMPILER", self.compiler.cxx)
        env.set("KOKKOS_CXX", self.compiler.cxx)
        env.set("MPICH_CXX", wrapper)
        env.set("OMPI_CXX", wrapper)
        env.set("MPICXX_CXX", wrapper)  # HPE MPT

    def setup_dependent_package(self, module, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        self.spec.kokkos_cxx = wrapper
