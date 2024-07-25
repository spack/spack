# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class RustProcMacro2(CargoPackage):
    """A substitute implementation of the compiler's `proc_macro` API to decouple token-based libraries from the procedural macro use case."""

    homepage = "https://docs.rs/proc-macro2/latest/proc_macro2/"
    url = "https://github.com/dtolnay/proc-macro2/archive/refs/tags/1.0.86.tar.gz"

    license("APACHE-2.0 OR MIT", checked_by="teaguesterling")

    version("1.0.86", sha256="b2af44ee7481c36c713338d093e534696b175697b1ef178d68f3f356e4732966")
    version("1.0.78", sha256="1ef81093cbe0ba5a3d073aba698c445a3188ae0ae55c58ee3294088d9f641883")
    version("1.0.77", sha256="ec779f2b2183c57bb61c062e94d82250016daa31cafd22fa396e2717b00f4437")
    version("1.0.60", sha256="f2d226f479fab5f82b97dfc16b93973807fd9d181c440bae5db393f042b09cdc")
