# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsoduration(PythonPackage):
    """Operations with ISO 8601 durations."""

    homepage = "https://github.com/bolsote/isoduration"
    pypi = "isoduration/isoduration-20.11.0.tar.gz"

    license("0BSD")

    version(
        "20.11.0",
        sha256="b2904c2a4228c3d44f409c8ae8e2370eb21a26f7ac2ec5446df141dde3452042",
        url="https://pypi.org/packages/7b/55/e5326141505c5d5e34c5e0935d2908a74e4561eca44108fbfb9c13d2911a/isoduration-20.11.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-arrow@0.15:")
