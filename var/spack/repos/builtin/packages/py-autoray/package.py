# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAutoray(PythonPackage):
    """Write backend agnostic numeric code compatible with any numpy-ish array library."""

    homepage = "https://github.com/jcmgray/autoray"
    pypi = "autoray/autoray-0.5.3.tar.gz"

    version("0.5.3", sha256="ecbecbc1ab65dd704234b3307fa7c7a511a36f6b9339a0ffcdaa4e5a7aab826b")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
