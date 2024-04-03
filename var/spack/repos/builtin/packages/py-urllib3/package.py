# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3(PythonPackage):
    """HTTP library with thread-safe connection pooling, file post, and
    more."""

    homepage = "https://urllib3.readthedocs.io/"
    pypi = "urllib3/urllib3-1.25.6.tar.gz"
    git = "https://github.com/urllib3/urllib3.git"

    license("MIT")

    version(
        "2.1.0",
        sha256="55901e917a5896a349ff771be919f8bd99aff50b79fe58fec595eb37bbc56bb3",
        url="https://pypi.org/packages/96/94/c31f58c7a7f470d5665935262ebd7455c7e4c7782eb525658d3dbf4b9403/urllib3-2.1.0-py3-none-any.whl",
    )
    version(
        "2.0.7",
        sha256="fdb6d215c776278489906c2f8916e6e7d4f5a9b602ccbcfdf7f016fc8da0596e",
        url="https://pypi.org/packages/d2/b2/b157855192a68541a91ba7b2bbcb91f1b4faa51f8bae38d8005c034be524/urllib3-2.0.7-py3-none-any.whl",
    )
    version(
        "2.0.6",
        sha256="7a7c7003b000adf9e7ca2a377c9688bbc54ed41b985789ed576570342a375cd2",
        url="https://pypi.org/packages/26/40/9957270221b6d3e9a3b92fdfba80dd5c9661ff45a664b47edd5d00f707f5/urllib3-2.0.6-py3-none-any.whl",
    )
    version(
        "2.0.5",
        sha256="ef16afa8ba34a1f989db38e1dbbe0c302e4289a47856990d0682e374563ce35e",
        url="https://pypi.org/packages/37/dc/399e63f5d1d96bb643404ee830657f4dfcf8503f5ba8fa3c6d465d0c57fe/urllib3-2.0.5-py3-none-any.whl",
    )
    version(
        "1.26.12",
        sha256="b930dd878d5a8afb066a637fbb35144fe7901e3b209d1cd4f524bd0e9deee997",
        url="https://pypi.org/packages/6f/de/5be2e3eed8426f871b170663333a0f627fc2924cc386cd41be065e7ea870/urllib3-1.26.12-py2.py3-none-any.whl",
    )
    version(
        "1.26.6",
        sha256="39fb8672126159acb139a7718dd10806104dec1e2f0f6c88aab05d17df10c8d4",
        url="https://pypi.org/packages/5f/64/43575537846896abac0b15c3e5ac678d787a4021e906703f1766bfb8ea11/urllib3-1.26.6-py2.py3-none-any.whl",
    )
    version(
        "1.25.11",
        sha256="f5321fbe4bf3fefa0efd0bfe7fb14e90909eb62a48ccda331726b4319897dd5e",
        url="https://pypi.org/packages/56/aa/4ef5aa67a9a62505db124a5cb5262332d1d4153462eb8fd89c9fa41e5d92/urllib3-1.25.11-py2.py3-none-any.whl",
    )
    version(
        "1.25.9",
        sha256="88206b0eb87e6d677d424843ac5209e3fb9d0190d0ee169599165ec25e9d9115",
        url="https://pypi.org/packages/e1/e5/df302e8017440f111c11cc41a6b432838672f5a70aa29227bf58149dc72f/urllib3-1.25.9-py2.py3-none-any.whl",
    )
    version(
        "1.25.6",
        sha256="3de946ffbed6e6746608990594d08faac602528ac7015ac28d33cee6a45b7398",
        url="https://pypi.org/packages/e0/da/55f51ea951e1b7c63a579c09dd7db825bb730ec1fe9c0180fc77bfb31448/urllib3-1.25.6-py2.py3-none-any.whl",
    )
    version(
        "1.25.3",
        sha256="b246607a25ac80bedac05c6f282e3cdaf3afb65420fd024ac94435cabe6e18d1",
        url="https://pypi.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl",
    )
    version(
        "1.24.3",
        sha256="a637e5fae88995b256e3409dc4d52c2e2e0ba32c42a6365fee8bbd2238de3cfb",
        url="https://pypi.org/packages/01/11/525b02e4acc0c747de8b6ccdab376331597c569c42ea66ab0a1dbd36eca2/urllib3-1.24.3-py2.py3-none-any.whl",
    )
    version(
        "1.21.1",
        sha256="8ed6d5c1ff9d6ba84677310060d6a3a78ca3072ce0684cb3c645023009c114b1",
        url="https://pypi.org/packages/24/53/f397db567de0aa0e81b211d81c13c41a779f14893e42189cf5bdb97611b2/urllib3-1.21.1-py2.py3-none-any.whl",
    )
    version(
        "1.20",
        sha256="b64c0faa183e9e9e76193146c4147e82a734982c6b6719dca851d6cc4ec90c01",
        url="https://pypi.org/packages/67/87/67be08389f8df83c9ba4c12e618a4ad93546e234a1e9530618735cd9b73d/urllib3-1.20-py2.py3-none-any.whl",
    )
    version(
        "1.14",
        sha256="ffe8859ca4fdfb021c2e8e0d3033f6c5eb372f8d4c3fd5455523055a2806a437",
        url="https://pypi.org/packages/73/55/63deba73d82dfa39974ca3903110c3e3557ff8758a3a79482810915b385d/urllib3-1.14-py2.py3-none-any.whl",
    )

    variant("brotli", default=False, when="@1.25:", description="Add Brotli support")
    variant("secure", default=False, when="@:2.0", description="Add SSL/TLS support")
    variant("socks", default=False, when="@1.15:", description="SOCKS and HTTP proxy support")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.1:")
        depends_on("python@3.7:", when="@2:2.0")
        depends_on("python@:3", when="@1.23:1.26.12")
        depends_on("py-brotli@1.0.9:", when="@1.26.9:+brotli")
        depends_on("py-brotlipy@0.6:", when="@1.25:1.26.8+brotli")
        depends_on("py-certifi", when="@1.13:2.0+secure")
        depends_on("py-cryptography@1.9:", when="@2.0.0-alpha2:2.0+secure")
        depends_on("py-cryptography@1.3.4:", when="@1.24:1.24.1,1.24.3:2.0.0-alpha1+secure")
        depends_on("py-idna@2:", when="@1.24:1.24.1,1.24.3:2.0+secure")
        depends_on("py-ipaddress", when="@1.24:1.24.1,1.24.3:1.24+secure")
        depends_on("py-pyopenssl@17.1:", when="@2.0.0-alpha2:2.0+secure")
        depends_on("py-pyopenssl@0.14:", when="@1.24:1.24.1,1.24.3:2.0.0-alpha1+secure")
        depends_on("py-pysocks@1.5.6,1.6:", when="@1.17:+socks")
        depends_on("py-urllib3-secure-extra", when="@1.26.12:2.0+secure")

    # Historical variant

    # Historical dependencies
