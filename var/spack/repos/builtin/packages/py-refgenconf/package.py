# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRefgenconf(PythonPackage):
    """A Python object for standardized reference genome assets."""

    homepage = "https://github.com/refgenie/refgenconf"
    pypi = "refgenconf/refgenconf-0.12.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.12.2",
        sha256="43be0120821b84a6480eb8bf23763c005df0a02f375aa2c1d318040711d26bb1",
        url="https://pypi.org/packages/b8/df/43109af627154773c5475e1031d1adf86bb117e8b72410c7b9dc00993c1d/refgenconf-0.12.2-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-future", when="@:0.9.1,0.10:")
        depends_on("py-jsonschema@3.0.1:", when="@0.10:")
        depends_on("py-pyfaidx", when="@0.9.1:")
        depends_on("py-pyyaml")
        depends_on("py-requests")
        depends_on("py-rich@9.0.1:", when="@0.10:")
        depends_on("py-tqdm", when="@0.12.1:")
        depends_on("py-yacman@0.8.3:", when="@0.12.2:")
