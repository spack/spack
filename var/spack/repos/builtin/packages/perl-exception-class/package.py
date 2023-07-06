# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExceptionClass(PerlPackage):
    """A module that allows you to declare real exception classes in Perl"""

    homepage = "https://metacpan.org/pod/Exception::Class"
    url = "http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Exception-Class-1.43.tar.gz"

    version("1.45", sha256="5482a77ef027ca1f9f39e1f48c558356e954936fc8fbbdee6c811c512701b249")
    version("1.43", sha256="ff3b4b3f706e84aaa87ab0dee5cec6bd7a8fc9f72cf76d115212541fa0a13760")

    depends_on("perl-devel-stacktrace", type=("build", "run"))
    depends_on("perl-class-data-inheritable", type=("build", "run"))
