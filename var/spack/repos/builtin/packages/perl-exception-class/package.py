# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExceptionClass(PerlPackage):
    """A module that allows you to declare real exception classes in Perl"""

    homepage = "https://metacpan.org/pod/Exception::Class"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Exception-Class-1.43.tar.gz"

    version("1.45", sha256="5482a77ef027ca1f9f39e1f48c558356e954936fc8fbbdee6c811c512701b249")
    version("1.44", sha256="33f3fbf8b138d3b04ea4ec0ba83fb0df6ba898806bcf4ef393d4cafc1a23ee0d")
    version("1.43", sha256="ff3b4b3f706e84aaa87ab0dee5cec6bd7a8fc9f72cf76d115212541fa0a13760")

    provides("perl-exception-class-base")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-devel-stacktrace@2.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-data-inheritable@0.2:", type="run")  # AUTO-CPAN2Spack
