# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesPsutil(PythonPackage):
    """Typing stubs for psutil."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-psutil/types-psutil-5.9.5.5.tar.gz"

    version("5.9.5.5", sha256="4f26fdb2cb064b274cbc6359fba4abf3b3a2993d7d4abc336ad0947568212c62")

    depends_on("py-setuptools", type="build")
