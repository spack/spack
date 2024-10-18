# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sccache(CargoPackage):
    """Sccache is a ccache-like tool. It is used as a compiler wrapper and avoids
    compilation when possible. Sccache has the capability to utilize caching in
    remote storage environments, including various cloud storage options, or
    alternatively, in local storage."""

    homepage = "https://github.com/mozilla/sccache"
    url = "https://github.com/mozilla/sccache/archive/refs/tags/v0.8.2.tar.gz"

    license("Apache-2.0", checked_by="pranav-sivaraman")

    version("0.8.2", sha256="2b3e0ef8902fe7bcdcfccf393e29f4ccaafc0194cbb93681eaac238cdc9b94f8")

    depends_on("rust@1.75:", when="@0.8.2:")
