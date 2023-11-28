# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libksba(AutotoolsPackage):
    """Libksba is a library to make the tasks of working with X.509
    certificates, CMS data and related objects easier.
    """

    homepage = "https://gnupg.org/software/libksba/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libksba/libksba-1.3.5.tar.bz2"

    maintainers("alalazo")

    version("1.6.5", sha256="a564628c574c99287998753f98d750babd91a4e9db451f46ad140466ef2a6d16")
    version("1.6.4", sha256="bbb43f032b9164d86c781ffe42213a83bf4f2fee91455edfa4654521b8b03b6b")
    version("1.6.3", sha256="3f72c68db30971ebbf14367527719423f0a4d5f8103fc9f4a1c01a9fa440de5c")

    # Deprecated over CVE-2022-3515 (https://gnupg.org/blog/20221017-pepe-left-the-ksba.html)
    version(
        "1.6.2",
        sha256="fce01ccac59812bddadffacff017dac2e4762bdb6ebc6ffe06f6ed4f6192c971",
        deprecated=True,
    )
    version(
        "1.6.0",
        sha256="dad683e6f2d915d880aa4bed5cea9a115690b8935b78a1bbe01669189307a48b",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="b0f4c65e4e447d9a2349f6b8c0e77a28be9531e4548ba02c545d1f46dc7bf921",
        deprecated=True,
    )
    version(
        "1.5.0",
        sha256="ae4af129216b2d7fdea0b5bf2a788cd458a79c983bb09a43f4d525cc87aba0ba",
        deprecated=True,
    )
    version(
        "1.4.0",
        sha256="bfe6a8e91ff0f54d8a329514db406667000cb207238eded49b599761bfca41b6",
        deprecated=True,
    )
    version(
        "1.3.5",
        sha256="41444fd7a6ff73a79ad9728f985e71c9ba8cd3e5e53358e70d5f066d35c1a340",
        deprecated=True,
    )

    depends_on("libgpg-error@1.8:")

    conflicts("%apple-clang@12:", when="@:1.3")

    def configure_args(self):
        return [
            "--enable-static",
            "--enable-shared",
            "--with-libgpg-error-prefix=" + self.spec["libgpg-error"].prefix,
        ]
