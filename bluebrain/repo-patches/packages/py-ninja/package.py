# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.py_ninja import PyNinja as BuiltinPyNinja


class PyNinja(BuiltinPyNinja):
    __doc__ = BuiltinPyNinja.__doc__

    version("1.11.1.1", sha256="9d793b08dd857e38d0b6ffe9e6b7145d7c485a42dcfea04905ca0cdb6017cc3c")
    depends_on("ninja@1.11.1", type=("build", "run"), when="@1.11.1.1")
