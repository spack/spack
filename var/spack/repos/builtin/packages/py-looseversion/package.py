# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLooseversion(PythonPackage):
    """Version numbering for anarchists and software realists."""

    homepage = "https://github.com/effigies/looseversion"
    pypi = "looseversion/looseversion-1.0.2.tar.gz"

    version("1.0.2", sha256="8b9f2e649eb81620c4527ba33ba87505eb69d4bb3f66523b34182a0450c294bc")

    depends_on("py-setuptools@40.8:", type="build")
