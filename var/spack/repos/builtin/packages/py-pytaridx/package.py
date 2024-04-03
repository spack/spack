# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytaridx(PythonPackage):
    """Python module/library for creating and maintaining a rapidly searchable
    index for a tar-file. This allows "direct access" of members (files) in
    the tar archive."""

    homepage = "https://github.com/LLNL/pytaridx"
    git = "https://github.com/LLNL/pytaridx.git"
    pypi = "pytaridx/pytaridx-1.0.2.tar.gz"

    maintainers("bhatiaharsh")

    license("MIT")

    version(
        "1.0.2",
        sha256="7a41b3adc398e8c0cafe8981d0690daa03d51cfd0bd41a6748f73f703a997ef7",
        url="https://pypi.org/packages/9b/05/60e76cb53b13a2b52bcfa21284845dc8b5a35e7d292a159d0ad48d4644cb/pytaridx-1.0.2-py3-none-any.whl",
    )
