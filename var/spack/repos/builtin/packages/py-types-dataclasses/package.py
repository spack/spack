# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTypesDataclasses(PythonPackage):
    """Typing stubs for dataclasses"""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-dataclasses/types-dataclasses-0.6.6.tar.gz"

    version(
        "0.6.6",
        sha256="a0a1ab5324ba30363a15c9daa0f053ae4fff914812a1ebd8ad84a08e5349574d",
        url="https://pypi.org/packages/31/85/23ab2bbc280266af5bf22ded4e070946d1694d1721ced90666b649eaa795/types_dataclasses-0.6.6-py3-none-any.whl",
    )
