# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlexx(PythonPackage):
    """Write desktop and web apps in pure Python."""

    homepage = "https://flexx.readthedocs.io"
    pypi = "flexx/flexx-0.4.1.zip"

    version(
        "0.4.1",
        sha256="f1ba68eb7de19bf1d270ba77232a24cf60d297d93b1ac9be6f47367a41b42b7d",
        url="https://pypi.org/packages/c3/f1/aff03c8b804e2c79a5a15c67c3eef7ff0f16a0ef9d06b0ec197421ced8bc/flexx-0.4.1-py2.py3-none-any.whl",
    )
