# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileWhich(PerlPackage):
    """Perl implementation of the which utility as an API"""

    homepage = "http://cpansearch.perl.org/src/PLICEASE/File-Which-1.22/lib/File/Which.pm"
    url = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Which-1.22.tar.gz"

    version("1.27", sha256="3201f1a60e3f16484082e6045c896842261fc345de9fb2e620fd2a2c7af3a93a")
    version("1.26_01", sha256="6bb26c65271c6fb7c8d9116adf5054197dea841648dd78fcbb327938fd48d1ef")
    version("1.25_01", sha256="a4323645686592a23b08fec9efad2d63d97455570c06566fcb3c2f5cd0b20263")
    version("1.24", sha256="7c5414dd6d5c61cb992fdd257aefe52f9a80bf55158cd5ec17469199d0b12eef")
    version("1.23", sha256="b79dc2244b2d97b6f27167fc3b7799ef61a179040f3abd76ce1e0a3b0bc4e078")
    version("1.22", sha256="e8a8ffcf96868c6879e82645db4ff9ef00c2d8a286fed21971e7280f52cf0dd4")

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
