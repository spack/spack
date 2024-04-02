# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHacking(PythonPackage):
    """OpenStack Hacking Guideline Enforcement."""

    homepage = "https://docs.openstack.org/hacking/latest/"
    pypi = "hacking/hacking-1.1.0.tar.gz"

    version(
        "1.1.0",
        sha256="d9ccda97228a46cbe562843469f3a82eb072f9ac1acefb4368c49a239bb19936",
        url="https://pypi.org/packages/71/05/ae66ec5a58e5c973ea09adcd4eac1a63e370579b768a2fd875172b8cc82e/hacking-1.1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-flake8@2.6:2", when="@1.1:1")
        depends_on("py-pbr@2:2.0,3:", when="@1.1:1")
        depends_on("py-six@1.10:", when="@1.1:3.0.0")
