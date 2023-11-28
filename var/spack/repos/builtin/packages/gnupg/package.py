# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import is_system_path


class Gnupg(AutotoolsPackage):
    """GNU Pretty Good Privacy (PGP) package."""

    homepage = "https://gnupg.org/index.html"
    url = "https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.3.4.tar.bz2"

    maintainers("alalazo")

    version("2.4.3", sha256="a271ae6d732f6f4d80c258ad9ee88dd9c94c8fdc33c3e45328c4d7c126bd219d")
    version("2.4.2", sha256="97eb47df8ae5a3ff744f868005a090da5ab45cb48ee9836dbf5ee739a4e5cf49")
    version("2.4.1", sha256="76b71e5aeb443bfd910ce9cbc8281b617c8341687afb67bae455877972b59de8")
    version("2.4.0", sha256="1d79158dd01d992431dd2e3facb89fdac97127f89784ea2cb610c600fb0c1483")
    version("2.3.8", sha256="540b7a40e57da261fb10ef521a282e0021532a80fd023e75fb71757e8a4969ed")
    version("2.3.7", sha256="ee163a5fb9ec99ffc1b18e65faef8d086800c5713d15a672ab57d3799da83669")
    version("2.2.40", sha256="1164b29a75e8ab93ea15033300149e1872a7ef6bdda3d7c78229a735f8204c28")

    # Deprecated over CVE-2022-34903
    version(
        "2.3.4",
        sha256="f3468ecafb1d7f9ad7b51fd1db7aebf17ceb89d2efa8a05cf2f39b4d405402ae",
        deprecated=True,
    )
    version(
        "2.3.3",
        sha256="5789b86da6a1a6752efb38598f16a77af51170a8494039c3842b085032e8e937",
        deprecated=True,
    )
    version(
        "2.3.2",
        sha256="e1d953e0e296072fca284215103ef168885eaac596c4660c5039a36a83e3041b",
        deprecated=True,
    )
    version(
        "2.3.1",
        sha256="c498db346a9b9a4b399e514c8f56dfc0a888ce8f327f10376ff984452cd154ec",
        deprecated=True,
    )
    version(
        "2.2.27",
        sha256="34e60009014ea16402069136e0a5f63d9b65f90096244975db5cea74b3d02399",
        deprecated=True,
    )
    version(
        "2.2.25",
        sha256="c55307b247af4b6f44d2916a25ffd1fb64ce2e509c3c3d028dbe7fbf309dc30a",
        deprecated=True,
    )
    version(
        "2.2.24",
        sha256="9090b400faae34f08469d78000cfec1cee5b9c553ce11347cc96ef16eab98c46",
        deprecated=True,
    )
    version(
        "2.2.23",
        sha256="10b55e49d78b3e49f1edb58d7541ecbdad92ddaeeb885b6f486ed23d1cd1da5c",
        deprecated=True,
    )
    version(
        "2.2.22",
        sha256="7c1370565e1910b9d8c4e0fb57b9de34aa062ec7bb91abad5803d791f38d855b",
        deprecated=True,
    )
    version(
        "2.2.21",
        sha256="61e83278fb5fa7336658a8b73ab26f379d41275bb1c7c6e694dd9f9a6e8e76ec",
        deprecated=True,
    )
    version(
        "2.2.20",
        sha256="04a7c9d48b74c399168ee8270e548588ddbe52218c337703d7f06373d326ca30",
        deprecated=True,
    )
    version(
        "2.2.19",
        sha256="242554c0e06f3a83c420b052f750b65ead711cc3fddddb5e7274fcdbb4e9dec0",
        deprecated=True,
    )
    version(
        "2.2.17",
        sha256="afa262868e39b651a2db4c071fba90415154243e83a830ca00516f9a807fd514",
        deprecated=True,
    )
    version(
        "2.2.15",
        sha256="cb8ce298d7b36558ffc48aec961b14c830ff1783eef7a623411188b5e0f5d454",
        deprecated=True,
    )
    version(
        "2.2.3",
        sha256="cbd37105d139f7aa74f92b6f65d136658682094b0e308666b820ae4b984084b4",
        deprecated=True,
    )
    version(
        "2.1.21",
        sha256="7aead8a8ba75b69866f583b6c747d91414d523bfdfbe9a8e0fe026b16ba427dd",
        deprecated=True,
    )

    version(
        "1.4.23",
        sha256="c9462f17e651b6507848c08c430c791287cd75491f8b5a8b50c6ed46b12678ba",
        deprecated=True,
    )

    depends_on("npth@1.2:", when="@2:")

    depends_on("libgpg-error@1.24:", when="@2:")
    depends_on("libgpg-error@1.41:", when="@2.3:")

    depends_on("libgcrypt@1.7.0:", when="@2:")
    depends_on("libgcrypt@1.9.1:", when="@2.3:")

    depends_on("libksba@1.3.4:", when="@2.0.0:")
    depends_on("libassuan@2.4:", when="@2.0.0:2.2.3")
    depends_on("libassuan@2.5:", when="@2.2.15:")
    depends_on("pinentry", type="run", when="@2:")
    depends_on("iconv", when="@2:")
    depends_on("zlib-api")

    depends_on("gawk", type="build", when="@:1")
    # note: perl and curl are gnupg1 dependencies when keyserver support is
    # requested, but we disable that.

    # Getting some linking error.
    conflicts("%gcc@10:", when="@:1")

    @run_after("install")
    def add_gpg2_symlink(self):
        if self.spec.satisfies("@2.0:2"):
            symlink("gpg", self.prefix.bin.gpg2)

    def configure_args(self):
        args = [
            "--disable-nls",
            "--disable-bzip2",
            "--disable-ldap",
            "--disable-regex",
            "--with-zlib=" + self.spec["zlib-api"].prefix,
            "--without-tar",
            "--without-readline",
        ]

        if self.spec.satisfies("@2:"):
            args.extend(
                [
                    "--disable-sqlite",
                    "--disable-ntbtls",
                    "--disable-gnutls",
                    "--with-pinentry-pgm=" + self.spec["pinentry"].command.path,
                    "--with-libgpg-error-prefix=" + self.spec["libgpg-error"].prefix,
                    "--with-libgcrypt-prefix=" + self.spec["libgcrypt"].prefix,
                    "--with-libassuan-prefix=" + self.spec["libassuan"].prefix,
                    "--with-ksba-prefix=" + self.spec["libksba"].prefix,
                    "--with-npth-prefix=" + self.spec["npth"].prefix,
                ]
            )
            if self.spec["iconv"].name == "libc":
                args.append("--without-libiconv-prefix")
            elif not is_system_path(self.spec["iconv"].prefix):
                args.append("--with-libiconv-prefix=" + self.spec["iconv"].prefix)

        if self.spec.satisfies("@:1"):
            args.extend(
                [
                    "--disable-agent-support",
                    "--disable-card-support",
                    "--disable-photo-viewers",
                    "--disable-exec",
                    "--disable-keyserver-path",
                    "--disable-keyserver-helpers",
                    "--disable-gnupg-iconv",
                    "--disable-dns-srv",
                    "--disable-dns-cert",
                    "--disable-gnupg-iconv",
                ]
            )

        if self.run_tests:
            args.append("--enable-all-tests")

        return args
