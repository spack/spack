# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyaml(PythonPackage):
    """PyYAML-based python module to produce pretty and readable
    YAML-serialized data."""

    maintainers("Kerilk", "liuyangzhuan")

    homepage = "https://github.com/mk-fg/pretty-yaml"
    pypi = "pyaml/pyaml-21.8.3.tar.gz"

    license("WTFPL")

    version(
        "21.8.3",
        sha256="aa61d6ebef7cd8ec691620616258d904bfbc152e9cf44557202b8bacc9ce5cce",
        url="https://pypi.org/packages/7b/33/12e2e89527df0e1f5bc07f94a039b981cc4a15f040f29a6cc978f8f99dd4/pyaml-21.8.3-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pyyaml", when="@21:")
