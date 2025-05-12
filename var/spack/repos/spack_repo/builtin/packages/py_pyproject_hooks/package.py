# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprojectHooks(PythonPackage):
    """Wrappers to call pyproject.toml-based build backend hooks."""

    homepage = "https://github.com/pypa/pyproject-hooks"
    pypi = "pyproject_hooks/pyproject_hooks-1.0.0.tar.gz"

    license("MIT")

    version("1.2.0", sha256="1e859bd5c40fae9448642dd871adf459e5e2084186e8d2c2a79a824c970da1f8")
    version("1.1.0", sha256="4b37730834edbd6bd37f26ece6b44802fb1c1ee2ece0e54ddff8bfc06db86965")
    version("1.0.0", sha256="f271b298b97f5955d53fb12b72c1fb1948c22c1a6b70b315c54cedaca0264ef5")

    depends_on("py-flit-core@3.2:3", type="build")
    depends_on("py-tomli@1.1:", when="@1.0.0 ^python@:3.10", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
