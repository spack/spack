# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBarectf(PythonPackage):
    """barectf (from bare metal and CTF) is a generator of
    tracer which produces CTF data streams."""

    pypi = "barectf/barectf-3.1.2.tar.gz"

    license("MIT")

    version(
        "3.1.2",
        sha256="e8efe74a1def51e4a288eec379fc85ba93d796dec6b65f958cbe53d827ca0023",
        url="https://pypi.org/packages/94/c2/9f423d775cfe5dcbace2510e642a3c136b228c024a05460f06f410f2bc2f/barectf-3.1.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@3:")
        depends_on("py-jinja2@3.0.0:", when="@3.0.2:")
        depends_on("py-jsonschema@3.2:3", when="@3:")
        depends_on("py-pyyaml@5.3:5", when="@3:")
        depends_on("py-setuptools", when="@3:")
        depends_on("py-termcolor@1.1:1", when="@3:")
