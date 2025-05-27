# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTld(PythonPackage):
    """Extract the top-level domain (TLD) from the URL given."""

    homepage = "https://github.com/barseghyanartur/tld"
    pypi = "tld/tld-0.13.1.tar.gz"

    version("0.13.1", sha256="75ec00936cbcf564f67361c41713363440b6c4ef0f0c1592b5b0fbe72c17a350")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
