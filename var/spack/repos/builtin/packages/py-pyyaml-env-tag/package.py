# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyyamlEnvTag(PythonPackage):
    """A custom YAML tag for referencing environment variables in YAML files."""

    homepage = "https://github.com/waylan/pyyaml-env-tag"
    pypi = "pyyaml_env_tag/pyyaml_env_tag-0.1.tar.gz"

    license("MIT")

    version(
        "0.1",
        sha256="af31106dec8a4d68c60207c1886031cbf839b68aa7abccdb19868200532c2069",
        url="https://pypi.org/packages/5a/66/bbb1dd374f5c870f59c5bb1db0e18cbe7fa739415a24cbd95b2d1f5ae0c4/pyyaml_env_tag-0.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-pyyaml")
