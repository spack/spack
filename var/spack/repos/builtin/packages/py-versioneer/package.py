# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVersioneer(PythonPackage):
    """Versioneer is a tool to automatically update version strings by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/python-versioneer/python-versioneer"
    pypi = "versioneer/versioneer-0.26.tar.gz"
    git = "https://github.com/python-versioneer/python-versioneer.git"

    maintainers("scemama")

    license("Unlicense")

    version(
        "0.29",
        sha256="0f1a137bb5d6811e96a79bb0486798aeae9b9c6efc24b389659cebb0ee396cb9",
        url="https://pypi.org/packages/b0/79/f0f1ca286b78f6f33c521a36b5cbd5bd697c0d66217d8856f443aeb9dd77/versioneer-0.29-py3-none-any.whl",
    )
    version(
        "0.28",
        sha256="11ffc09427ac99db4ce61bdc85785dae819618d0de28153adfce3085956125a8",
        url="https://pypi.org/packages/97/9c/cb00da3e038a90ab850f6d70eeddd0c78e1575e59f329b8f7a820d66a9bf/versioneer-0.28-py3-none-any.whl",
    )
    version(
        "0.27",
        sha256="525c66e285691087d2418c3226c346c23b59d96fe7ab612369e05f22321b32af",
        url="https://pypi.org/packages/83/66/4189e7b76adaeeb125a93a89cb13f3b79a6f709aa5ad87478ff229e37820/versioneer-0.27-py3-none-any.whl",
    )
    version(
        "0.26",
        sha256="67f464f152283caaec2c0fdd9f2f782bb460932c155bcc9529daa1bec84f26f6",
        url="https://pypi.org/packages/3f/fb/70545da549f3a75821e1c2078f351dfb9cbb4bfa18cd47890366759fb6ba/versioneer-0.26-py3-none-any.whl",
    )
    version(
        "0.18",
        sha256="08e395c0acc544f78645b9c0ebfccaf47950ae61e0c85bd1aaea98ff59609aeb",
        url="https://pypi.org/packages/95/b5/8bcf39663abc1fda6a2af6704062a44be13d3bc1ceca562a9c020fae8f36/versioneer-0.18-py2.py3-none-any.whl",
    )

    variant("toml", default=True, description="Install TOML support", when="@0.26:")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.23:")
        depends_on("py-tomli", when="@0.28:+toml ^python@:3.10")
        depends_on("py-tomli", when="@0.26:0.27+toml")
