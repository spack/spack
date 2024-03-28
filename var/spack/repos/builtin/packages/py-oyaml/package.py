# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOyaml(PythonPackage):
    """Ordered YAML: a drop-in replacement for PyYAML which preserves dict ordering."""

    homepage = "https://github.com/wimglenn/oyaml"
    pypi = "oyaml/oyaml-1.0.tar.gz"

    license("MIT")

    version(
        "1.0",
        sha256="3a378747b7fb2425533d1ce41962d6921cda075d46bb480a158d45242d156323",
        url="https://pypi.org/packages/37/aa/111610d8bf5b1bb7a295a048fc648cec346347a8b0be5881defd2d1b4a52/oyaml-1.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyyaml")
