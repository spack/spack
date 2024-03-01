# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
from llnl.util import tty

from spack.package import *


class AoclCrypto(CMakePackage):
    """
    AOCL-Crypto is a library consisting of basic cryptographic functions
    optimized and tuned for AMD Zen™ based microarchitecture.

    This library provides a unified solution for Cryptographic routines such
    as AES (Advanced Encryption Standard) encryption/decryption routines
    (CFB, CTR, CBC, CCM, GCM, OFB, SIV, XTS), SHA (Secure Hash Algorithms)
    routines (SHA2, SHA3, SHAKE), Message Authentication Code (CMAC, HMAC),
    ECDH (Elliptic-curve Diffie–Hellman) and RSA (Rivest, Shamir, and Adleman)
    key generation functions, etc. AOCL Crypto supports a dynamic dispatcher
    feature that executes the most optimal function variant implemented using
    Function Multi-versioning thereby offering a single optimized library
    portable across different x86 CPU architectures.

    AOCL Crypto framework is developed in C / C++ for Unix and Windows based
    systems.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-Cryptography license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/cryptography/eula/cryptography-4-2-eula.html
    """

    _name = "aocl-crypto"
    homepage = "https://www.amd.com/en/developer/aocl/cryptography.html"
    git = "https://github.com/amd/aocl-crypto"
    url = "https://github.com/amd/aocl-crypto/archive/refs/tags/4.2.tar.gz"

    maintainers("amd-toolchain-support")
    version(
        "4.2",
        sha256="2bdbedd8ab1b28632cadff237f4abd776e809940ad3633ad90fc52ce225911fe",
        preferred=True,
    )
    variant("examples", default=False, description="Build examples")

    depends_on("cmake@3.15:", type="build")
    depends_on("openssl@3.0.0:")
    depends_on("p7zip", type="build")
    for vers in ["4.2"]:
        with when(f"@={vers}"):
            depends_on(f"aocl-utils@={vers}")

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        build_directory = self.stage.source_path

        if self.spec.variants["build_type"].value == "Debug":
            build_directory = join_path(build_directory, "build", "debug")
        else:
            build_directory = join_path(build_directory, "build", "release")

        return build_directory

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec
        if not (
            spec.satisfies(r"%aocc@4.1:4.2")
            or spec.satisfies(r"%gcc@12.2:13.1")
            or spec.satisfies(r"%clang@16:17")
        ):
            tty.warn(
                "AOCL has been tested to work with the following compilers "
                "versions - gcc@12.2:13.1, aocc@4.1:4.2, and clang@16:17 "
                "see the following aocl userguide for details: "
                "https://www.amd.com/content/dam/amd/en/documents/developer/version-4-2-documents/aocl/aocl-4-2-user-guide.pdf"
            )

        args = ["-DCMAKE_C_COMPILER=%s" % spack_cc, "-DCMAKE_CXX_COMPILER=%s" % spack_cxx]
        args.append(self.define_from_variant("ALCP_ENABLE_EXAMPLES", "examples"))
        args.append("-DOPENSSL_INSTALL_DIR=" + spec["openssl"].prefix)
        args.append("-DENABLE_AOCL_UTILS=ON")
        args.append("-DAOCL_UTILS_INSTALL_DIR=" + spec["aocl-utils"].prefix)

        return args
