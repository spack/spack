# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libassuan(AutotoolsPackage):
    """Libassuan is a small library implementing the so-called Assuan
    protocol.
    """

    homepage = "https://gnupg.org/software/libassuan/index.html"
    url = "https://gnupg.org/ftp/gcrypt/libassuan/libassuan-2.4.5.tar.bz2"

    maintainers("alalazo")

    version("2.5.6", sha256="e9fd27218d5394904e4e39788f9b1742711c3e6b41689a31aa3380bd5aa4f426")
    version("2.5.5", sha256="8e8c2fcc982f9ca67dcbb1d95e2dc746b1739a4668bc20b3a3c5be632edb34e4")
    version("2.5.4", sha256="c080ee96b3bd519edd696cfcebdecf19a3952189178db9887be713ccbcb5fbf0")
    version("2.5.3", sha256="91bcb0403866b4e7c4bc1cc52ed4c364a9b5414b3994f718c70303f7f765e702")
    version("2.4.5", sha256="fbfea5d1dbcdee34f2597b0afb3d8bb4eda96c924a1e01b01c2acde68b81625f")
    version("2.4.3", sha256="22843a3bdb256f59be49842abf24da76700354293a066d82ade8134bb5aa2b71")

    depends_on("libgpg-error@1.17:")

    def configure_args(self):
        return [
            "--enable-static",
            "--enable-shared",
            "--with-libgpg-error-prefix=" + self.spec["libgpg-error"].prefix,
        ]
