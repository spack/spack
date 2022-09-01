# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlUri(PerlPackage):
    """Uniform Resource Identifiers (absolute and relative)"""

    homepage = "https://metacpan.org/pod/URI"
    url = "https://cpan.metacpan.org/authors/id/O/OA/OALDERS/URI-5.12.tar.gz"

    version("5.12", sha256="66abe0eaddd76b74801ecd28ec1411605887550fc0a45ef6aa744fdad768d9b3")
    version("5.11", sha256="d3b62a69a6ab288021167d428ac4673c399d42e4de69eb49c7953a30821843c9")
    version("5.10", sha256="16325d5e308c7b7ab623d1bf944e1354c5f2245afcfadb8eed1e2cae9a0bd0b5")
    version("5.09", sha256="03e63ada499d2645c435a57551f041f3943970492baa3b3338246dab6f1fae0a")
    version(
        "5.08",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-5.08.tar.gz",
        sha256="7e2c6fe3b1d5947da334fa558a96e748aaa619213b85bcdce5b5347d4d26c46e",
    )
    version("1.76", sha256="b2c98e1d50d6f572483ee538a6f4ccc8d9185f91f0073fd8af7390898254413e")
    version("1.75", sha256="bdfcee61ca7f390b0fe68b98a52f7e96b827a4e918a7727f87f8b3e56f5cb440")
    version(
        "1.74",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.74.tar.gz",
        sha256="a9c254f45f89cb1dd946b689dfe433095404532a4543bdaab0b71ce0fdcdd53d",
    )
    version(
        "1.73",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.73.tar.gz",
        sha256="cca7ab4a6f63f3ccaacae0f2e1337e8edf84137e73f18548ec7d659f23efe413",
    )
    version(
        "1.72",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.72.tar.gz",
        sha256="35f14431d4b300de4be1163b0b5332de2d7fbda4f05ff1ed198a8e9330d40a32",
    )
    version(
        "1.71",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/URI-1.71.tar.gz",
        sha256="9c8eca0d7f39e74bbc14706293e653b699238eeb1a7690cc9c136fb8c2644115",
    )

    provides("perl-uri-escape")  # AUTO-CPAN2Spack
    provides("perl-uri-heuristic")  # AUTO-CPAN2Spack
    provides("perl-uri-iri")  # AUTO-CPAN2Spack
    provides("perl-uri-queryparam")  # AUTO-CPAN2Spack
    provides("perl-uri-split")  # AUTO-CPAN2Spack
    provides("perl-uri-url")  # AUTO-CPAN2Spack
    provides("perl-uri-withbase")  # AUTO-CPAN2Spack
    provides("perl-uri-data")  # AUTO-CPAN2Spack
    provides("perl-uri-file")  # AUTO-CPAN2Spack
    provides("perl-uri-file-base")  # AUTO-CPAN2Spack
    provides("perl-uri-file-fat")  # AUTO-CPAN2Spack
    provides("perl-uri-file-mac")  # AUTO-CPAN2Spack
    provides("perl-uri-file-os2")  # AUTO-CPAN2Spack
    provides("perl-uri-file-qnx")  # AUTO-CPAN2Spack
    provides("perl-uri-file-unix")  # AUTO-CPAN2Spack
    provides("perl-uri-file-win32")  # AUTO-CPAN2Spack
    provides("perl-uri-ftp")  # AUTO-CPAN2Spack
    provides("perl-uri-gopher")  # AUTO-CPAN2Spack
    provides("perl-uri-http")  # AUTO-CPAN2Spack
    provides("perl-uri-https")  # AUTO-CPAN2Spack
    provides("perl-uri-ldap")  # AUTO-CPAN2Spack
    provides("perl-uri-ldapi")  # AUTO-CPAN2Spack
    provides("perl-uri-ldaps")  # AUTO-CPAN2Spack
    provides("perl-uri-mailto")  # AUTO-CPAN2Spack
    provides("perl-uri-mms")  # AUTO-CPAN2Spack
    provides("perl-uri-news")  # AUTO-CPAN2Spack
    provides("perl-uri-nntp")  # AUTO-CPAN2Spack
    provides("perl-uri-nntps")  # AUTO-CPAN2Spack
    provides("perl-uri-pop")  # AUTO-CPAN2Spack
    provides("perl-uri-rlogin")  # AUTO-CPAN2Spack
    provides("perl-uri-rsync")  # AUTO-CPAN2Spack
    provides("perl-uri-rtsp")  # AUTO-CPAN2Spack
    provides("perl-uri-rtspu")  # AUTO-CPAN2Spack
    provides("perl-uri-sftp")  # AUTO-CPAN2Spack
    provides("perl-uri-sip")  # AUTO-CPAN2Spack
    provides("perl-uri-sips")  # AUTO-CPAN2Spack
    provides("perl-uri-snews")  # AUTO-CPAN2Spack
    provides("perl-uri-ssh")  # AUTO-CPAN2Spack
    provides("perl-uri-telnet")  # AUTO-CPAN2Spack
    provides("perl-uri-tn3270")  # AUTO-CPAN2Spack
    provides("perl-uri-urn")  # AUTO-CPAN2Spack
    provides("perl-uri-urn-isbn")  # AUTO-CPAN2Spack
    provides("perl-uri-urn-oid")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-test-needs", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="run")  # AUTO-CPAN2Spack
