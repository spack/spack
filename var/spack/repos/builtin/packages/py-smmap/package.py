# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmmap(PythonPackage):
    """
    A pure Python implementation of a sliding window memory map manager
    """

    homepage = "https://github.com/gitpython-developers/smmap"
    pypi = "smmap/smmap-3.0.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.0.0",
        sha256="2aba19d6a040e78d8b09de5c57e96207b09ed71d8e55ce0959eeee6c8e190d94",
        url="https://pypi.org/packages/6d/01/7caa71608bc29952ae09b0be63a539e50d2484bc37747797a66a60679856/smmap-5.0.0-py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="a9a7479e4c572e2e775c404dcd3080c8dc49f39918c2cf74913d30c4c478e3c2",
        url="https://pypi.org/packages/68/ee/d540eb5e5996eb81c26ceffac6ee49041d473bc5125f2aa995cf51ec1cf1/smmap-4.0.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.5",
        sha256="7bfcf367828031dc893530a29cb35eb8c8f2d7c8f2d0989354d75d24c8573714",
        url="https://pypi.org/packages/d5/1e/6130925131f639b2acde0f7f18b73e33ce082ff2d90783c436b52040af5a/smmap-3.0.5-py2.py3-none-any.whl",
    )
    version(
        "3.0.4",
        sha256="54c44c197c819d5ef1991799a7e30b662d1e520f2ac75c9efbeb54a742214cf4",
        url="https://pypi.org/packages/b0/9a/4d409a6234eb940e6a78dfdfc66156e7522262f5f2fecca07dc55915952d/smmap-3.0.4-py2.py3-none-any.whl",
    )
