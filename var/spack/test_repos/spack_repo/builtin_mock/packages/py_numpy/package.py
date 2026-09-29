# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package
from spack_repo.builtin_mock.build_systems.python import PythonExtension

from spack.package import *


class PyNumpy(Package, PythonExtension):
    """A package which extends python, depends on C and C++, and has a pure build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/py-numpy-1.0.tar.gz"

    version("2.3.4", md5="00000000000000000000000000000120")

    extends("python")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake", type="build")
