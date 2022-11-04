# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RemoveReplaceDependency(Package):
    """Test removing and replacing dependencies,
    dropping conflicts and patches"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", "abcdef0123456789abcdef0123456789")

    depends_on("things@1.0:")
    drop_dependency("things")

    depends_on("stuff@1.0:")
    drop_dependency("stuff")
    depends_on("stuff")

    conflicts("%gcc")
    drop_conflict("%gcc")

    patch("foo.patch")
    patch("bar.patch")
    patch(
        "http://example.com/baz.patch",
        sha256="ea8fac7c65fb589b0d53560f5251f74f9e9b243478dcb6b3ea79b5e36449c8d9",
    )
    patch(
        "http://example.com/bing.patch",
        sha256="ea8fac7c65fb589b0d53560f5251f74f9e9b243478dcb6b3ea79b5e36449c8d9",
    )
    drop_patch("foo.patch")
    drop_patch("http://example.com/baz.patch")
