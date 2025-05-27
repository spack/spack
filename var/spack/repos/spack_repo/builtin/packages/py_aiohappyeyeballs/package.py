# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyAiohappyeyeballs(PythonPackage):
    """This library exists to allow connecting with Happy Eyeballs (RFC 8305)
    when you already have a list of addrinfo and not a DNS name."""

    homepage = "https://github.com/aio-libs/aiohappyeyeballs"
    pypi = "aiohappyeyeballs/aiohappyeyeballs-2.6.1.tar.gz"

    version("2.6.1", sha256="c3f9d0113123803ccadfdf3f0faa505bc78e6a72d1cc4806cbd719826e943558")

    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-poetry-core@2:", type="build", when="@2.4.5:")
    depends_on("python@3.9:", when="@2.4.5:", type=("build", "run"))
