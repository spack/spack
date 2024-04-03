# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDjango(PythonPackage):
    """The Web framework for perfectionists with deadlines."""

    homepage = "https://www.djangoproject.com/"
    url = "https://github.com/django/django/archive/3.0.5.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.0.5",
        sha256="642d8eceab321ca743ae71e0f985ff8fdca59f07aab3a9fb362c617d23e33a76",
        url="https://pypi.org/packages/a9/4f/8a247eee2958529a6a805d38fbacd9764fd566462fa0016aa2a2947ab2a6/Django-3.0.5-py3-none-any.whl",
    )
    version(
        "3.0.4",
        sha256="89e451bfbb815280b137e33e454ddd56481fdaa6334054e6e031041ee1eda360",
        url="https://pypi.org/packages/12/68/8c125da33aaf0942add5095a7a2a8e064b3812d598e9fb5aca9957872d71/Django-3.0.4-py3-none-any.whl",
    )
    version(
        "3.0.3",
        sha256="c91c91a7ad6ef67a874a4f76f58ba534f9208412692a840e1d125eb5c279cb0a",
        url="https://pypi.org/packages/c6/b7/63d23df1e311ca0d90f41352a9efe7389ba353df95deea5676652e615420/Django-3.0.3-py3-none-any.whl",
    )
    version(
        "3.0.2",
        sha256="4f2c913303be4f874015993420bf0bd8fd2097a9c88e6b49c6a92f9bdd3fb13a",
        url="https://pypi.org/packages/55/d1/8ade70e65fa157e1903fe4078305ca53b6819ab212d9fbbe5755afc8ea2e/Django-3.0.2-py3-none-any.whl",
    )
    version(
        "3.0.1",
        sha256="b61295749be7e1c42467c55bcabdaee9fbe9496fdf9ed2e22cef44d9de2ff953",
        url="https://pypi.org/packages/6a/23/08f7fd7afdd24184a400fcaebf921bd09b5b5235cbd62ffa02308a7d35d6/Django-3.0.1-py3-none-any.whl",
    )
    version(
        "2.2.12",
        sha256="6ecd229e1815d4fc5240fc98f1cca78c41e7a8cd3e3f2eefadc4735031077916",
        url="https://pypi.org/packages/af/d1/903cdbda68cd6ee74bf8ac7c86ffa04b2baf0254dfd6edeeafe4426c9c8b/Django-2.2.12-py3-none-any.whl",
    )
    version(
        "2.2.11",
        sha256="b51c9c548d5c3b3ccbb133d0bebc992e8ec3f14899bce8936e6fdda6b23a1881",
        url="https://pypi.org/packages/be/76/7ccbcf52366590ca76997ce7860308b257b79962a4e4fada5353f72d7be5/Django-2.2.11-py3-none-any.whl",
    )
    version(
        "2.2.10",
        sha256="9a4635813e2d498a3c01b10c701fe4a515d76dd290aaa792ccb65ca4ccb6b038",
        url="https://pypi.org/packages/2b/b2/eb6230a30a5cc3a71b4df733de95c1a888e098e60b5e233703936f9c4dad/Django-2.2.10-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-asgiref@3.2:", when="@3.0")
        depends_on("py-pytz", when="@:3")
        depends_on("py-sqlparse@0.2.2:", when="@2.2.14:2,3.0-rc1:4.2-beta1")
        depends_on("py-sqlparse", when="@:2.2.13,3:3.0-beta1")
