# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFqdn(PythonPackage):
    """Validates fully-qualified domain names against RFC 1123, so that they
    are acceptable to modern bowsers."""

    homepage = "https://github.com/ypcrts/fqdn"
    pypi = "fqdn/fqdn-1.5.1.tar.gz"

    license("MPL-2.0")

    version(
        "1.5.1",
        sha256="3a179af3761e4df6eb2e026ff9e1a3033d3587bf980a0b1b2e1e5d08d7358014",
        url="https://pypi.org/packages/cf/58/8acf1b3e91c58313ce5cb67df61001fc9dcd21be4fadb76c1a2d540e09ed/fqdn-1.5.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@1.5:")
        depends_on("py-cached-property@1.3:", when="@1.4: ^python@:3.7")
