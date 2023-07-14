# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3(PythonPackage):
    """HTTP library with thread-safe connection pooling, file post, and
    more."""

    homepage = "https://urllib3.readthedocs.io/"
    pypi = "urllib3/urllib3-1.25.6.tar.gz"

    version("2.0.3", sha256="bee28b5e56addb8226c96f7f13ac28cb4c301dd5ea8a6ca179c0b9835e032825")
    version("1.26.16", sha256="8f135f6502756bde6b2a9b28989df5fbe87c9970cecaa69041edcce7f0589b14")
    version("1.26.12", sha256="3fa96cf423e6987997fc326ae8df396db2a8b7c667747d47ddd8ecba91f4a74e")
    version("1.26.6", sha256="f57b4c16c62fa2760b7e3d97c35b255512fb6b59a259730f36ba32ce9f8e342f")
    version("1.25.9", sha256="3018294ebefce6572a474f0604c2021e33b3fd8006ecd11d62107a5d2a963527")
    version("1.25.6", sha256="9a107b99a5393caf59c7aa3c1249c16e6879447533d0887f4336dde834c7be86")
    version("1.25.3", sha256="dbe59173209418ae49d485b87d1681aefa36252ee85884c31346debd19463232")
    version("1.24.3", sha256="2393a695cd12afedd0dcb26fe5d50d0cf248e5a66f75dbd89a3d4eb333a61af4")
    version("1.21.1", sha256="b14486978518ca0901a76ba973d7821047409d7f726f22156b24e83fd71382a5")
    version("1.20", sha256="97ef2b6e2878d84c0126b9f4e608e37a951ca7848e4855a7f7f4437d5c34a72f")
    version("1.14", sha256="dd4fb13a4ce50b18338c7e4d665b21fd38632c5d4b1d9f1a1379276bd3c08d37")

    variant("socks", default=False, description="SOCKS and HTTP proxy support")
    variant("secure", default=False, description="Add SSL/TLS support", when="@:2.0")
    variant("brotli", default=False, description="Add Brotli support")
    variant("zstd", default=False, description="Add Zstandard support", when="@2:")

    depends_on("python@2.7:2.8,3.4:", when="@:1.25", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@1.26.6", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:3", when="@1.26.12:", type=("build", "run"))
    depends_on("python@3.7:3", when="@2:", type=("build", "run"))

    depends_on("py-setuptools", when="@1", type="build")
    depends_on("py-hatchling@1.6.0:1", when="@2", type="build")

    depends_on("py-pyopenssl@0.14:", when="+secure")
    depends_on("py-pyopenssl@17.1.0:", when="+secure @2:")
    depends_on("py-cryptography@1.3.4:", when="+secure")
    depends_on("py-cryptography@1.9:", when="+secure @2:")
    depends_on("py-idna@2:", when="+secure")
    depends_on("py-certifi", when="+secure")
    depends_on("py-urllib3-secure-extra", when="+secure @1.26.12:")

    depends_on("py-pysocks@1.5.6,1.5.8:1", when="+socks")

    depends_on("py-brotlipy@0.6:", when="+brotli @:1")
    depends_on("py-brotlicffi@1.0.9:", when="+brotli @2:")

    depends_on("py-zstandard@0.18.0:", when="+zstd @2:")
