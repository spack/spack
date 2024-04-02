# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAltair(PythonPackage):
    """Declarative statistical visualization library for Python"""

    pypi = "altair/altair-5.2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.2.0",
        sha256="8c4888ad11db7c39f3f17aa7f4ea985775da389d79ac30a6c22856ab238df399",
        url="https://pypi.org/packages/c5/e4/7fcceef127badbb0d644d730d992410e4f3799b295c9964a172f92a469c7/altair-5.2.0-py3-none-any.whl",
    )
    version(
        "5.1.2",
        sha256="7219708ec33c152e53145485040f428954ed15fd09b2a2d89e543e6d111dae7f",
        url="https://pypi.org/packages/17/16/b12fca347ff9d062e3c44ad9641d2ec50364570a059f3078ada3a5119d7a/altair-5.1.2-py3-none-any.whl",
    )
    version(
        "5.1.1",
        sha256="bb421459b53c80ad45f2bd009c87da2a81165b8f7d5a90658e0fc1ffc741bf34",
        url="https://pypi.org/packages/f2/b4/02a0221bd1da91f6e6acdf0525528db24b4b326a670a9048da474dfe0667/altair-5.1.1-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="af1d502fa27a400ab4c82c55a185b4eaa74f1146f619e53278ba19934e90510a",
        url="https://pypi.org/packages/2b/40/ff33821bca16cac30f8d9c3244ac961416f40bf2d3261a1250aabda33a6f/altair-5.1.0-py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="9f3552ed5497d4dfc14cf48a76141d8c29ee56eae2873481b4b28134268c9bbe",
        url="https://pypi.org/packages/b2/20/5c3b89d6f8d9938325a9330793438389e0dc94c34d921f6da35ec62095f3/altair-5.0.1-py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="e7deed321f61a3ec752186ae96e97b44a1353de142928c1934fb211e9f0bfe9e",
        url="https://pypi.org/packages/2e/b8/49d377d9a7a85dc24e35d70384fc5ae7b19db6f8ee9d23d36337675c602e/altair-5.0.0-py3-none-any.whl",
    )
    version(
        "4.2.2",
        sha256="8b45ebeaf8557f2d760c5c77b79f02ae12aee7c46c27c06014febab6f849bc87",
        url="https://pypi.org/packages/18/62/47452306e84d4d2e67f9c559380aeb230f5e6ca84fafb428dd36b96a99ba/altair-4.2.2-py3-none-any.whl",
    )
    version(
        "4.2.1",
        sha256="67e099a651c78028c4e135e3b5bd9680ed7dd928ca7b61c9c7376c58e41d2b02",
        url="https://pypi.org/packages/17/18/1e20c890bc12dfdd633cc58d76101fd544cc8f58fc316f2f6e13c6a83af2/altair-4.2.1-py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="0c724848ae53410c13fa28be2b3b9a9dcb7b5caa1a70f7f217bd663bb419935a",
        url="https://pypi.org/packages/0a/fb/56aaac0c69d106e380ff868cd5bb6cccacf2b8917a8527532bc89804a52e/altair-4.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5.1:")
        depends_on("python@3.7:", when="@4.2:5.0")
        depends_on("py-entrypoints", when="@:4")
        depends_on("py-importlib-metadata", when="@5:5.0 ^python@:3.7")
        depends_on("py-jinja2")
        depends_on("py-jsonschema@3.0.0:", when="@4.2.0:5.0.0-rc2,5.0.0:")
        depends_on("py-numpy")
        depends_on("py-packaging", when="@5.1:")
        depends_on("py-pandas@0.25.0:", when="@5.1:")
        depends_on("py-pandas@0.18:", when="@4.1:5.0")
        depends_on("py-toolz")
        depends_on("py-typing-extensions@4.0.1:", when="@5: ^python@:3.10")
