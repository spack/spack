# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFaustCchardet(PythonPackage):
    """C-based character encoding detector."""

    homepage = "https://github.com/faust-streaming/cChardet"
    pypi = "faust-cchardet/faust-cchardet-2.1.19.tar.gz"

    maintainers("thomas-bouvier")

    version("2.1.19", sha256="f89386297cde0c8e0f5e21464bc2d6d0e4a4fc1b1d77cdb238ca24d740d872e0")

    depends_on("py-setuptools", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-cython", type="build")
    depends_on("pkgconfig", type="build")
