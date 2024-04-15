# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMsgpackNumpy(PythonPackage):
    """This package provides encoding and decoding routines
    that enable the serialization and deserialization of
    numerical and array data types provided by numpy using the
    highly efficient msgpack format. Serialization of Python's
    native complex data types is also supported."""

    homepage = "https://github.com/lebedov/msgpack-numpy"
    pypi = "msgpack-numpy/msgpack-numpy-0.4.7.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.4.7.1",
        sha256="50d9e456d034ead6de53d9596a64bac4c9b0e15a682c4dce0efc556dc9d786fe",
        url="https://pypi.org/packages/19/05/05b8d7c69c6abb36a34325cc3150089bdafc359f0a81fb998d93c5d5c737/msgpack_numpy-0.4.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.4.7",
        sha256="609ecb02389c8858ec095dc7587fb45e9cfc4630ef725442b84dbbd77221bd57",
        url="https://pypi.org/packages/57/8c/901d65deb827c0d9f7680ea808a0d63eab71fbfac5c6a868b6c9e92be4cb/msgpack_numpy-0.4.7-py2.py3-none-any.whl",
    )
    version(
        "0.4.6",
        sha256="6902ca9f7208095f00ed91f3843ddc6dfe2e95f31dfff672f09b617d4b740108",
        url="https://pypi.org/packages/07/b9/3d9bff29e914e1a2e1a2edbbfcec8b89a6bdaa3a94bd87d37e8202337873/msgpack_numpy-0.4.6-py2.py3-none-any.whl",
    )
    version(
        "0.4.5",
        sha256="d3875ea0015b42e1e2ebe8b111d9fdbc8f11efe0f55644a255cc95a01d78d23d",
        url="https://pypi.org/packages/4b/32/323eda6da56cdbf768e41858d491c163a6989f27b1733eb3e9fca21291aa/msgpack_numpy-0.4.5-py2.py3-none-any.whl",
    )
    version(
        "0.4.4.3",
        sha256="ae5f04d4a2274d14549dd057f3ae03a0523700a13dae3e906ddaf2a6d2844400",
        url="https://pypi.org/packages/c8/ab/09904a909bccc471f219fb8f5d0838cbcb10cc26089a2b29e84c893e216e/msgpack_numpy-0.4.4.3-py2.py3-none-any.whl",
    )
    version(
        "0.4.4.2",
        sha256="20d3f679cd727e2b9acb59297988895a148add8995618e7437b80bb95e7a0d7d",
        url="https://pypi.org/packages/b4/1c/68fcaeb72ac4a9c7f44cf4d19082bd4e486cd035134b118ddea6eff10e7d/msgpack_numpy-0.4.4.2-py2.py3-none-any.whl",
    )
    version(
        "0.4.4.1",
        sha256="31b1b165431766e8ba12ab0a5af80c1681859c00af6e002f785ddb8d468d507c",
        url="https://pypi.org/packages/bb/a9/2a28ef55c9b2c197d8531bb9c05adce2ba454d37ca8d26c1d421c4945b0d/msgpack_numpy-0.4.4.1-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-msgpack@0.5.2:", when="@0.4.4.1:")
        depends_on("py-numpy@1.9:", when="@0.4.2:")
