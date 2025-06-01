# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyahocorasick(PythonPackage):
    """Fast and memory efficient library for exact or approximate
    multi-pattern string search."""

    homepage = "http://github.com/WojciechMula/pyahocorasick"
    pypi = "pyahocorasick/pyahocorasick-2.1.0.tar.gz"

    version("2.1.0", sha256="4df4845c1149e9fa4aa33f0f0aa35f5a42957a43a3d6e447c9b44e679e2672ea")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Optional dependencies for testing
    depends_on("py-pytest", type="test")
    depends_on("py-twine", type="test")
    depends_on("py-wheel", type="test")

    def build_args(self, spec, prefix):
        args = []
        # By default, build as unicode (matches setup.py behavior)
        args.append("--define-macros=AHOCORASICK_UNICODE")
        return args
