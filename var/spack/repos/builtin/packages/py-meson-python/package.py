# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMesonPython(PythonPackage):
    """Meson Python build backend (PEP 517)."""

    homepage = "https://github.com/mesonbuild/meson-python"
    pypi = "meson_python/meson_python-0.7.0.tar.gz"

    maintainers("eli-schwartz", "adamjstewart", "rgommers")

    license("MIT")

    version(
        "0.15.0",
        sha256="3ae38253ff02b2e947a05e362a2eaf5a9a09d133c5666b4123399ee5fbf2e591",
        url="https://pypi.org/packages/1f/60/b10b11ab470a690d5777310d6cfd1c9bdbbb0a1313a78c34a1e82e0b9d27/meson_python-0.15.0-py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="e33ea3efbadecc15768c205d03b905c7b3bf72afae1e1ebd84b438c4a3ed3393",
        url="https://pypi.org/packages/9f/af/5f941f57dc516e72b018183a38fbcfb018a7e83afd3c756ecfba82f21c65/meson_python-0.13.1-py3-none-any.whl",
    )
    version(
        "0.12.0",
        sha256="3a2e7bfabf37f1878ad7b5556399deaf2dbffead85a50fc681a8bd4f4ef63da5",
        url="https://pypi.org/packages/ee/22/da1cc8cafca80283c795ebf58d4218017225df8288d70cb8fc32eb46f5e0/meson_python-0.12.0-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="78bde58c88b2fa7691fcb1a97daa0a75f33a76f2ada9d605b75d70dd6505b48f",
        url="https://pypi.org/packages/3d/e9/01bc1bf0a5feaaac504e1e5ad5a8b24088729103fb7229f57fb5c248b2a5/meson_python-0.11.0-py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="98889e7ba2fcf88aef9b07029cca2d6533ffa5ff2fe0aafa98c31b0fa049a5d4",
        url="https://pypi.org/packages/8f/5a/ac172d2a0d8ce77d3a1eda4b30ffcf7419af7dd74e428286a554e5456c32/meson_python-0.10.0-py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="1e3aa60fb8d93f63b9e56dfd7cb6bbd57466455d0c052b6522c80af369ab7eb5",
        url="https://pypi.org/packages/3f/96/fa15f7376fcbe5e1217023181a7d3a70b384993fd44a469041ab186d7af4/meson_python-0.9.0-py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="9a3e21b2cebc84a4d411534cb6f955b4bfcd9720a506cf834f3f745b24622727",
        url="https://pypi.org/packages/a9/0f/d634169ccdb4bbd9b1b2e649f20969793be82fd24757ba0eac895903c2e2/meson_python-0.8.1-py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="eac1829b93c55c2c9407ac65ed295013fd251251a2e81526d3232ac65c3555f6",
        url="https://pypi.org/packages/03/b7/906d43aeccdd0baff85e089e75661684903cffe7d1ae29767c1b264d3df3/meson_python-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="bb16595b08606e67b5439e0bfac6ecb2d794e82e36fc38889ba8417a7ad5b15d",
        url="https://pypi.org/packages/c6/00/5b680cf929c31fd3d1d0b001c458b2ce241085c2d3800608016f23377949/meson_python-0.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("meson@0.63.3:", when="@0.15: ^python@:3.11")
        depends_on("meson@1.2.3:", when="@0.15: ^python@3.12:")
        depends_on("meson@0.63.3:", when="@0.11:0.14")
        depends_on("meson@0.62.0:", when="@0.8.1:0.10")
        depends_on("meson@0.60.0:", when="@:0.8.0")
        depends_on("py-ninja", when="@:0.10")
        depends_on("py-pyproject-metadata@0.7.1:", when="@0.13.0:")
        depends_on("py-pyproject-metadata@0.6.1:", when="@0.12:0.13.0-rc0")
        depends_on("py-pyproject-metadata@0.5:", when="@0.6:0.11")
        depends_on("py-setuptools@60:", when="@0.13.0:0.14 ^python@3.12:")
        depends_on("py-tomli@1:", when="@0.11: ^python@:3.10")
        depends_on("py-tomli@1:", when="@:0.10")
        depends_on("py-typing-extensions@3.7.4:", when="@0.12 ^python@:3.9")

        # marker: os_name == "nt"
        # depends_on("py-colorama", when="@0.3:")

    # https://github.com/mesonbuild/meson-python/pull/111
    conflicts("platform=darwin os=ventura", when="@:0.7")
    conflicts("platform=darwin os=monterey", when="@:0.7")
    conflicts("platform=darwin os=bigsur", when="@:0.7")

    # Historical dependencies
