# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlMoo(PerlPackage):
    """Minimalist Object Orientation (with Moose compatibility)."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/H/HA/HAARG"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-2.005004.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version(
        "2.005.004",
        sha256="e3030b80bd554a66f6b3c27fd53b1b5909d12af05c4c11ece9a58f8d1e478928",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-2.005004.tar.gz",
    )
    version(
        "2.005.003",
        sha256="bcb5ff4a4f806647ce16e1cbf85bdc0ab5d1e7ae3dc224ab6bcc774bc2e82b43",
        url="https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-2.005003.tar.gz",
    )

    provides("perl-method-generate-accessor")  # AUTO-CPAN2Spack
    provides("perl-method-generate-buildall")  # AUTO-CPAN2Spack
    provides("perl-method-generate-constructor")  # AUTO-CPAN2Spack
    provides("perl-method-generate-demolishall")  # AUTO-CPAN2Spack
    provides("perl-moo-handlemoose")  # AUTO-CPAN2Spack
    provides("perl-moo-handlemoose-fakeconstructor")  # AUTO-CPAN2Spack
    provides("perl-moo-handlemoose-fakemetaclass")  # AUTO-CPAN2Spack
    provides("perl-moo-handlemoose--typemap")  # AUTO-CPAN2Spack
    provides("perl-moo-object")  # AUTO-CPAN2Spack
    provides("perl-moo-role")  # AUTO-CPAN2Spack
    provides("perl-moo--utils")  # AUTO-CPAN2Spack
    provides("perl-moo-sification")  # AUTO-CPAN2Spack
    provides("perl-oo")  # AUTO-CPAN2Spack

    depends_on("perl@5.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-method-modifiers@1.10:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-class-xsaccessor@1.18:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-exporter-tiny", type=("build", "run"))
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-role-tiny@2.2.3:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util@1.0:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-defer@2.6.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-quote@2.6.6:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sub-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-test-fatal@0.3:", type=("build", "test"))  # AUTO-CPAN2Spack
