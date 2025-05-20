# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PySalib(PythonPackage):
    """Python implementations of commonly used sensitivity analysis methods."""

    homepage = "https://salib.readthedocs.org"
    pypi = "salib/salib-1.4.6.tar.gz"

    maintainers("schmitts")

    license("MIT")

    version("1.5.1", sha256="e4a9c319b8dd02995a8dc983f57c452cb7e5b6dbd43e7b7856c90cb6a332bb5f")
    version("1.5.0", sha256="04367cbe7f63c5206ec0d793b80477bb4d61d50c0b8c76db1844fe8709f7a39c")
    version("1.4.8", sha256="86e7cca79f73f3c52825101cacfb2d51d95adfb7771e7e0ebcd632bffa2cab82")
    version("1.4.7", sha256="2e6cb19ec772d6cb7368feceae0f61e51f2d6afdbc4f8986a780b87d657b38cc")
    version("1.4.6.1", sha256="dbb14bfc25debf24192feac98cd34c167fbed42743afbcd614cbeb625f310d69")
    version("1.4.6", sha256="14337239f1e92960e8f53774c27b1d072253790b57edbbebd290057a5eeb3858")
    version(
        "1.4.4",
        sha256="50a6459088700f55261a683752818530d14ede30cece2c324ac94d4b9e288b6d",
        url="https://files.pythonhosted.org/packages/SALib/SALib-1.4.4.tar.gz",
    )
    version(
        "1.4.0.1",
        sha256="dbf6e865af9f3be82a79cf64889ed66d6d3b6803f0c22a242a112876789d49e7",
        url="https://files.pythonhosted.org/packages/source/s/SALib/SALib-1.4.0.1.tar.gz",
    )

    variant("distributed", default=False, description="Build with experimental distributed mode")

    depends_on("py-importlib-metadata", type="build", when="@1.4.4:1.4.5 ^python@:3.7")
    depends_on("py-setuptools@38.3:", type="build", when="@:1.4.5")
    depends_on("py-setuptools-scm", type="build", when="@1.4.4:1.4.5")
    depends_on("py-wheel", type="build", when="@:1.4.5")
    depends_on("py-hatchling@1.8.1:", type="build", when="@1.4.6:")
    depends_on("py-hatch-vcs", type="build", when="@1.5.0:")

    depends_on("python@3.9:", type=("build", "run"), when="@1.5.0:")
    depends_on("python@3.8:", type=("build", "run"), when="@1.4.6:")
    depends_on("py-numpy@1.20.3:", type=("build", "run"), when="@1.4.6:")
    depends_on("py-numpy@1.16.5:", type=("build", "run"))
    depends_on("py-scipy@1.9.3:", type=("build", "run"), when="@1.5.0:")
    depends_on("py-scipy@1.7.3:", type=("build", "run"), when="@1.4.6:")
    depends_on("py-scipy@1.5.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.5:", type=("build", "run"), when="@1.5.0:")
    depends_on("py-matplotlib@3.2.2:", type=("build", "run"), when="@:1.4.8")
    depends_on("py-pandas@2.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("py-pandas@1.2:", type=("build", "run"), when="@1.4.8:")
    depends_on("py-pandas@1.1.2:", type=("build", "run"))
    depends_on("py-pathos@0.3.2:", type=("build", "run"), when="@1.5.0: +distributed")
    depends_on("py-pathos@0.2.5:", type=("build", "run"), when="@1.4.6: +distributed")
    depends_on("py-pathos@0.2.5:", type=("build", "run"), when="@:1.4.5")
