# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Azcopy(Package):
    """AzCopy is a command-line utility that you can use to copy data to and from containers and
    file shares in Azure Storage accounts.
    """

    homepage = "https://github.com/Azure/azure-storage-azcopy"
    url = "https://github.com/Azure/azure-storage-azcopy/archive/refs/tags/v10.18.1.tar.gz"

    version("10.18.1", sha256="80292625d7f1a6fc41688c5948b3a20cfdae872464d37d831e20999430819c3f")

    depends_on("go", type="build")

    def install(self, spec, prefix):
        go("build", "-o", prefix.bin.azcopy)
