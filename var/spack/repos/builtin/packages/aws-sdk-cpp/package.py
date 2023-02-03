# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AwsSdkCpp(CMakePackage):
    """AWS SDK for C++.

    The AWS SDK for C++ provides a modern C++ (version C++ 11 or later) interface for
    Amazon Web Services (AWS). It is meant to be performant and fully functioning with
    low- and high-level SDKs, while minimizing dependencies and providing platform
    portability (Windows, OSX, Linux, and mobile).
    """

    homepage = "https://github.com/aws/aws-sdk-cpp"
    git = "https://github.com/aws/aws-sdk-cpp.git"

    version("1.10.32", tag="1.10.32", submodules=True)
    version("1.9.247", tag="1.9.247", submodules=True)

    depends_on("cmake@3.1:", type="build")
    depends_on("zlib")
    depends_on("curl")

    # https://github.com/aws/aws-sdk-cpp/issues/1816
    patch(
        "https://github.com/aws/aws-sdk-cpp/pull/1937.patch?full_index=1",
        sha256="ba86e0556322604fb4b70e2dd4f4fb874701868b07353fc1d5c329d90777bf45",
        when="@1.9.247",
    )
