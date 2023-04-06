# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlAck(PerlPackage):
    """A grep-like program for searching source code."""  # AUTO-CPAN2Spack

    homepage = "https://beyondgrep.com/"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/ack-v3.6.0.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("3.6.0", sha256="03144d1070649e92f6a1b7d20bdc535e2bb1ac258daabe482e9aa8277b48f005")
    version("3.5.0", sha256="66053e884e803387a02ddee0d68abf2a10239fab654364dab33287309a725521")

    provides("perl-app-ack")  # AUTO-CPAN2Spack
    provides("perl-app-ack-configdefault")  # AUTO-CPAN2Spack
    provides("perl-app-ack-configfinder")  # AUTO-CPAN2Spack
    provides("perl-app-ack-configloader")  # AUTO-CPAN2Spack
    provides("perl-app-ack-file")  # AUTO-CPAN2Spack
    provides("perl-app-ack-files")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-collection")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-default")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-extension")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-extensiongroup")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-firstlinematch")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-inverse")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-is")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-isgroup")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-ispath")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-ispathgroup")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-match")  # AUTO-CPAN2Spack
    provides("perl-app-ack-filter-matchgroup")  # AUTO-CPAN2Spack
    depends_on("perl@5.10.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-harness@2.50:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-file-next@1.18:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-list-util", type="run")  # AUTO-CPAN2Spack
