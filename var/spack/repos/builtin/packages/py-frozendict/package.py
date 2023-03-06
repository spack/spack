# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFrozendict(PythonPackage):
    """An immutable dictionary"""

    homepage = "An immutable dictionary"
    pypi = "frozendict/frozendict-1.2.tar.gz"

    version("2.3.4", sha256="15b4b18346259392b0d27598f240e9390fafbff882137a9c48a1e0104fb17f78")
    version("1.2", sha256="774179f22db2ef8a106e9c38d4d1f8503864603db08de2e33be5b778230f6e45")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
