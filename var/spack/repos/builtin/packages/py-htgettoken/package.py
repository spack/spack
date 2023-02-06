# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtgettoken(PythonPackage):
    """htgettoken gets OIDC authentication tokens for High Throughput Computing
    via a Hashicorp vault server."""

    homepage = "https://github.com/fermitools/htgettoken"

    # htgettoken is not available on PyPi
    url = "https://github.com/fermitools/htgettoken/archive/refs/tags/v1.16.tar.gz"
    git = "https://github.com/fermitools/htgettoken.git"

    maintainers("wdconinc")

    # The following versions refer to setuptools-buildable commits after 1.16;
    # they are special reproducible version numbers from `git describe`
    version("1.16-33-g3788bb4", commit="3788bb4733e5e8f856cee51566df9a36cbfe097d")
    version("1.16-20-g8b72f48", commit="8b72f4800ef99923dac99dbe0756a26266a27886")
    # Older versions do not have a python build system but included for completeness
    version(
        "1.16",
        sha256="984fd4746082086356d968b4db536f7b35d30e65a6589fa357caa3266cb98268",
        deprecated=True,
    )

    depends_on("py-setuptools", type="build")

    depends_on("py-gssapi", type="run")
    depends_on("py-paramiko", type="run")
    depends_on("py-urllib3", type="run")

    def setup_run_environment(self, env):
        if env.get("XDG_RUNTIME_DIR") and env.get("UID"):
            env.set("BEARER_TOKEN", join_path(env.get("XDG_RUNTIME_DIR"), "bt_u" + env.get("UID")))
