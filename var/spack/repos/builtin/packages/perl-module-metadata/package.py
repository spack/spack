# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleMetadata(PerlPackage):
    """Gather package and POD information from perl module files."""  # AUTO-CPAN2Spack

    homepage = "https://github.com/Perl-Toolchain-Gang/Module-Metadata"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Metadata-1.000037.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "1.000.037",
        sha256="8d5a74c1b07e145edda254602fedf19c0dd0c2d9688a370afdaff89c32cba629",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Metadata-1.000037.tar.gz",
    )
    version(
        "1.000.036",
        sha256="1c70e438cec1f7f99a5cccd4529efb4ee0fb7ca958ca885ebf09952015b957aa",
        url="https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Metadata-1.000036.tar.gz",
    )

    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack

