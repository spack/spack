# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNanobind(PythonPackage):
    """nanobind -- Seamless operability between C++11 and Python.

    nanobind is a small binding library that exposes C++ types in
    Python and vice versa. It is reminiscent of Boost.Python and pybind11
    and uses near-identical syntax. In contrast to these existing tools,
    nanobind is more efficient: bindings compile in a shorter amount of time,
    produce smaller binaries, and have better runtime performance.
    """

    homepage = "https://nanobind.readthedocs.io"
    url = "https://github.com/wjakob/nanobind/archive/refs/tags/v1.2.0.tar.gz"
    git = "https://github.com/wjakob/nanobind.git"

    maintainers("chrisrichardson", "garth-wells", "ma595")

    license("BSD-3-Clause")

    version(
        "1.8.0",
        sha256="c9b069f408660124b12565ca026834d146154a3965efcd2bcf749eefb99b4873",
        url="https://pypi.org/packages/3f/35/73cb6560af76dc75257635875d033111f1ac324e1cfd4b953d442e874aac/nanobind-1.8.0-py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="a368b8121d3c1ec384a2dab0cb2b556924ceafc84ed80b0d1e211e3997576dae",
        url="https://pypi.org/packages/8c/cd/0520686bf2e367e6ef6fb11992161b5d8807a488fa9985572400816a8102/nanobind-1.7.0-py3-none-any.whl",
    )
    version(
        "1.6.2",
        sha256="27b62eae0134cd60563a4026e5f347d88fcae6d6357b11683b470eb4c51efe9f",
        url="https://pypi.org/packages/dc/79/343cdc299ce8d4569f906284492c31c62482d6fade5b53c9ecd818de5dc3/nanobind-1.6.2-py3-none-any.whl",
    )
    version(
        "1.5.2",
        sha256="34515bf2c0675d6d1c7be17ae8c7a1361439cb0a98dcde15899f23a63ef1b55f",
        url="https://pypi.org/packages/96/8a/fbabb2a18dbf16343ca34c6d6dcc019365f9683eb79d5cfcffe18a07689a/nanobind-1.5.2-py3-none-any.whl",
    )
    version(
        "1.5.1",
        sha256="e4408ca6bcd424cb4555c6217cf7624d334862a6d497c549b01b9bc509e25b21",
        url="https://pypi.org/packages/cd/90/300cac4677ffdd95c5fac9cd1a64348370ce7f5f30e6c1042642ad907b1f/nanobind-1.5.1-py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="0e23436bdc7246c332eb4bd477b89b53482490457a12d7b084a9b410f122770b",
        url="https://pypi.org/packages/ed/ea/5e806594f91cdbc00897acd990c2f5778f37bef0deb94ae03ac66cba4a1c/nanobind-1.5.0-py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="0eeded0d18368e2b575714dc620e85631ffe03eb719f8d629101abb2c09668d8",
        url="https://pypi.org/packages/67/ce/1b20a4c92f607eb7229775c0babb409484e5d62fcecc083f8d7d0a8b5270/nanobind-1.4.0-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="949332ba8653a7dedf1ebb24855a4479116e7774478240213a00493db3c49e9d",
        url="https://pypi.org/packages/a8/39/16ef46072bbfe55fcb5f7f0884befc06ffeae304c9ad1a2515029471c21b/nanobind-1.2.0-py3-none-any.whl",
    )

    @property
    def cmake_prefix_paths(self):
        paths = [join_path(self.prefix, self.spec["python"].package.platlib, "nanobind", "cmake")]
        return paths
