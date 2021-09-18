# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nextflow(Package):
    """Data-driven computational pipelines."""

    homepage = "https://www.nextflow.io"
    url      = "https://github.com/nextflow-io/nextflow/releases/download/v21.04.3/nextflow-21.04.3-all"

    maintainers = ['dialvarezs']

    version('21.04.3', sha256='6eed23699055af60a85dd017b0351b7151982c6440b1ec5c273c1d4d07567572', expand=False)
    version('20.10.0', sha256='ef6e229307f04a6abd27f06f7e999dc77e064ab94d0202243801f8b69bb3641c', expand=False)
    version('20.07.1', sha256='97f393248260c71bfc4e18b4e41005a4ca48b32ccc20f76c8d7e9a6d6dc43a33', expand=False)
    version('20.04.1', sha256='851f20884e50b0d0593a82786b8ded038c2e3b8c759275d01a5e98645abff640', expand=False)
    version('20.01.0', sha256='6b212d9e4206855165da4d96b23940a4979fa96dcd4e0cbe29633bd8e4f2ff5b', expand=False)
    version('19.10.0', sha256='6f14a35222791836b01f1be8e46925ce2d739618705cf81faf83d66faeb41778', expand=False)
    version('19.07.0', sha256='6f7069b43f395c5d902321745d37988fed7ef84d2006ea00be0df19de97c1986', expand=False)
    version('19.04.1', sha256='219e67098fc20dcd8144c1a6fad58c9b23677f833d71b7a2187d4d30c82517c4', expand=False)
    version('0.25.6', sha256='4a396544c603a2fba2cce6bf0be7ea21d32bff80ae8d727442b5ad98e4be861f', expand=False, deprecated=True)
    version('0.24.1', sha256='91ed989cf4241acac3eecfe025bc24db7c913468b86ce1a105d5468d6adfb5cf', expand=False, deprecated=True)
    version('0.23.3', sha256='74687406246162cb55edee459a9bac16d3ba9cebfd2ec3fa22bd109d6f0a4b06', expand=False, deprecated=True)
    version('0.21.0', sha256='4ad10c772c19a91ac0a707272bf76679ec89da7ec441c72d42d2e4ee73adea47', expand=False, deprecated=True)
    version('0.20.1', sha256='4f4bba43019395c7fc9425b8fab9ccb933dad0040e39b760279a4ea86e72829d', expand=False, deprecated=True)
    version('0.17.3', sha256='dac4bf2c7522620745d48ec61e68a22a3e668e51cff2f1582df90dadc4be9550', expand=False, deprecated=True)

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "nextflow"))
        set_executable(join_path(prefix.bin, "nextflow"))
