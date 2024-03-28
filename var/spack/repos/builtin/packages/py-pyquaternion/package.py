# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyquaternion(PythonPackage):
    """Python morphology manipulation toolkit"""

    homepage = "https://kieranwynn.github.io/pyquaternion/"
    pypi = "pyquaternion/pyquaternion-0.9.5.tar.gz"

    license("MIT")

    version(
        "0.9.5",
        sha256="bac5945d08b9a2f4106dc76206e40f353c7240fdf37a370e13b03113c135f59b",
        url="https://pypi.org/packages/83/e3/339e1135d94c2db689fbf33603cbc8f2861ca15a1dce79963f796b3cc910/pyquaternion-0.9.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@0.9.5:")
