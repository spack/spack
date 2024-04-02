# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyDocutils(PythonPackage):
    """Docutils is an open-source text processing system for processing
    plaintext documentation into useful formats, such as HTML, LaTeX,
    man-pages, open-document or XML. It includes reStructuredText, the
    easy to read, easy to use, what-you-see-is-what-you-get plaintext
    markup language."""

    homepage = "http://docutils.sourceforge.net/"
    pypi = "docutils/docutils-0.15.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.20.1",
        sha256="96f387a2c5562db4476f09f13bbab2192e764cac08ebbf3a34a95d9b1e4a59d6",
        url="https://pypi.org/packages/26/87/f238c0670b94533ac0353a4e2a1a771a0cc73277b88bff23d3ae35a256c1/docutils-0.20.1-py3-none-any.whl",
    )
    version(
        "0.19",
        sha256="5e1de4d849fee02c63b040a4a3fd567f4ab104defd8a5511fbbc24a8a017efbc",
        url="https://pypi.org/packages/93/69/e391bd51bc08ed9141ecd899a0ddb61ab6465309f1eb470905c0c8868081/docutils-0.19-py3-none-any.whl",
    )
    version(
        "0.18.1",
        sha256="23010f129180089fbcd3bc08cfefccb3b890b0050e1ca00c867036e9d161b98c",
        url="https://pypi.org/packages/8d/14/69b4bad34e3f250afe29a854da03acb6747711f3df06c359fa053fae4e76/docutils-0.18.1-py2.py3-none-any.whl",
    )
    version(
        "0.18",
        sha256="a31688b2ea858517fa54293e5d5df06fbb875fb1f7e4c64529271b77781ca8fc",
        url="https://pypi.org/packages/4c/42/5aefc2ffc563ef8456276430da8f045f55176c45746b0c3434c0c474c746/docutils-0.18-py2.py3-none-any.whl",
    )
    version(
        "0.17.1",
        sha256="cf316c8370a737a022b72b56874f6602acf974a37a9fba42ec2876387549fc61",
        url="https://pypi.org/packages/4c/5e/6003a0d1f37725ec2ebd4046b657abb9372202655f96e76795dca8c0063c/docutils-0.17.1-py2.py3-none-any.whl",
    )
    version(
        "0.17",
        sha256="a71042bb7207c03d5647f280427f14bfbd1a65c9eb84f4b341d85fafb6bb4bdf",
        url="https://pypi.org/packages/9a/65/76aea825b59727b556cca74e28d68e4d73244d2e1e8a8945c29d6d3d5e11/docutils-0.17-py2.py3-none-any.whl",
    )
    version(
        "0.16",
        sha256="0c5b78adfbf7762415433f5515cd5c9e762339e23369dbe8000d84a4bf4ab3af",
        url="https://pypi.org/packages/81/44/8a15e45ffa96e6cf82956dd8d7af9e666357e16b0d93b253903475ee947f/docutils-0.16-py2.py3-none-any.whl",
    )
    version(
        "0.15.2",
        sha256="6c4f696463b79f1fb8ba0c594b63840ebd41f059e92b31957c46b74a4599b6d0",
        url="https://pypi.org/packages/22/cd/a6aa959dca619918ccb55023b4cb151949c64d4d5d55b3f4ffd7eee0c6e8/docutils-0.15.2-py3-none-any.whl",
    )
    version(
        "0.14",
        sha256="02aec4bd92ab067f6ff27a38a38a41173bf01bed8f89157768c1573f53e474a6",
        url="https://pypi.org/packages/36/fa/08e9e6e0e3cbd1d362c3bbee8d01d0aedb2155c4ac112b19ef3cae8eed8d/docutils-0.14-py3-none-any.whl",
    )
    version(
        "0.13.1",
        sha256="cb3ebcb09242804f84bdbf0b26504077a054da6772c6f4d625f335cc53ebf94d",
        url="https://pypi.org/packages/7c/30/8fb30d820c012a6f701a66618ce065b6d61d08ac0a77e47fc7808dbaee47/docutils-0.13.1-py3-none-any.whl",
    )
    version(
        "0.12",
        sha256="dcebd4928112631626f4c4d0df59787c748404e66dda952110030ea883d3b8cd",
        url="https://pypi.org/packages/c7/16/29d8de2404c5b90243b51f91315b3ce375169ceb48a68aeec0862e0143c4/docutils-0.12-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.19-beta1:0.20")

    # Uses 2to3

    # Includes "longintrepr.h" instead of Python.h
    conflicts("^python@3.11:", when="@:0.15")

    # NOTE: This creates symbolic links to be able to run docutils scripts
    # without .py file extension similarly to various linux distributions to
    # increase compatibility with other packages
    @run_after("install")
    def post_install(self):
        bin_path = self.prefix.bin
        for file in os.listdir(bin_path):
            if file.endswith(".py"):
                os.symlink(os.path.join(bin_path, file), os.path.join(bin_path, file[:-3]))
