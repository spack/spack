# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from os import symlink

from spack.package import *


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"

    license("MIT")

    if platform.system() == "Linux" and platform.machine() == "x86_64":
        version(
            "6.0.25",
            url="https://download.visualstudio.microsoft.com/download/pr/1cac4d08-3025-4c00-972d-5c7ea446d1d7/a83bc5cbedf8b90495802ccfedaeb2e6/dotnet-sdk-6.0.417-linux-x64.tar.gz",
            sha256="1b7c5ea04ccb817e1a411c9e1f89d7a4e54c0842b01b457e141bbc254ce97ba2",
            preferred=True,
        )

        version(
            "6.0.2",
            url="https://download.visualstudio.microsoft.com/download/pr/e7acb87d-ab08-4620-9050-b3e80f688d36/e93bbadc19b12f81e3a6761719f28b47/dotnet-sdk-6.0.102-linux-x64.tar.gz",
            sha256="9bdd4dacdf9a23d386f207ec19260afd36a7fb7302233c9abc0b47e65ffc3119",
            deprecated=True,
        )

        version(
            "5.0.4",
            url="https://download.visualstudio.microsoft.com/download/pr/73a9cb2a-1acd-4d20-b864-d12797ca3d40/075dbe1dc3bba4aa85ca420167b861b6/dotnet-sdk-5.0.201-linux-x64.tar.gz",
            sha256="9ff77087831e8ca32719566ec9ef537e136cfc02c5ff565e53f5509cc6e7b341",
            deprecated=True,
        )

        version(
            "3.1.13",
            url="https://download.visualstudio.microsoft.com/download/pr/ab82011d-2549-4e23-a8a9-a2b522a31f27/6e615d6177e49c3e874d05ee3566e8bf/dotnet-sdk-3.1.407-linux-x64.tar.gz",
            sha256="a744359910206fe657c3a02dfa54092f288a44c63c7c86891e866f0678a7e911",
            deprecated=True,
        )

        version(
            "2.1.300",
            url="https://download.microsoft.com/download/8/8/5/88544F33-836A-49A5-8B67-451C24709A8F/dotnet-sdk-2.1.300-linux-x64.tar.gz",
            sha256="fabca4c8825182ff18e5a2f82dfe75aecd10260ee9e7c85a8c4b3d108e5d8e1b",
            deprecated=True,
        )
    elif platform.system() == "Linux" and platform.machine() == "aarch64":
        version(
            "6.0.25",
            url="https://download.visualstudio.microsoft.com/download/pr/03972b46-ddcd-4529-b8e0-df5c1264cd98/285a1f545020e3ddc47d15cf95ca7a33/dotnet-sdk-6.0.417-linux-arm64.tar.gz",
            sha256="c071e936442b90b80a941ab177b8c7851bc5377cf842cc1e61922b3d7fefeb0e",
            preferred=True,
        )

    variant("telemetry", default=False, description="allow collection of telemetry data")

    def setup_build_environment(self, env):
        if "-telemetry" in self.spec:
            env.set("DOTNET_CLI_TELEMETRY_OPTOUT", 1)

    def install(self, spec, prefix):
        mkdirp("bin")
        symlink("../dotnet", "bin/dotnet")
        install_tree(".", prefix)
