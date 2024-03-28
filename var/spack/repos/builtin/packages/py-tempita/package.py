# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTempita(PythonPackage):
    """A very small text templating language"""

    homepage = "https://pypi.org/project/Tempita"
    pypi = "tempita/Tempita-0.5.2.tar.gz"

    license("MIT")

    version(
        "0.5.2",
        sha256="f4554840cb59c6b4a5df4fad27eea4e3cb47ca7089bfeefb5890ff1bb8af2117",
        url="https://pypi.org/packages/46/5b/2ad80b580134a160e84b9aac0d136df3d77d5ccd45cd349f6146d41cee76/Tempita-0.5.2-py3-none-any.whl",
    )
