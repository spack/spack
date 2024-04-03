# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloI18n(PythonPackage):
    """
    The oslo.i18n library contain utilities for working with
    internationalization (i18n) features, especially translation for text
    strings in an application or library.
    """

    homepage = "https://docs.openstack.org/oslo.i18n"
    pypi = "oslo.i18n/oslo.i18n-5.0.1.tar.gz"

    maintainers("haampie")

    version(
        "5.0.1",
        sha256="99a6453b9b7a9d1603ba6c32e6ab8c738af95f6573215682a33c8028340bdccd",
        url="https://pypi.org/packages/89/ac/b71a66e54c8fcf22c4205efe2b5f94dbf282c194f9f07dbf0a1ac52d4633/oslo.i18n-5.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pbr@2:2.0,3:")
        depends_on("py-six@1.10:", when="@:5.0")
