# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecated(PythonPackage):
    """Python @deprecated decorator to deprecate old python classes,
    functions or methods."""

    homepage = "https://github.com/tantale/deprecated"
    pypi = "Deprecated/Deprecated-1.2.13.tar.gz"

    license("MIT")

    version(
        "1.2.13",
        sha256="64756e3e14c8c5eea9795d93c524551432a0be75629f8f29e67ab8caf076c76d",
        url="https://pypi.org/packages/51/6a/c3a0408646408f7283b7bc550c30a32cc791181ec4618592eec13e066ce3/Deprecated-1.2.13-py2.py3-none-any.whl",
    )
    version(
        "1.2.7",
        sha256="8b6a5aa50e482d8244a62e5582b96c372e87e3a28e8b49c316e46b95c76a611d",
        url="https://pypi.org/packages/f6/89/62912e01f3cede11edcc0abf81298e3439d9c06c8dce644369380ed13f6d/Deprecated-1.2.7-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-wrapt@1.10:", when="@1.2.6:")
