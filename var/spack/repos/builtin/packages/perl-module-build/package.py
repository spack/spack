# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleBuild(PerlPackage):
    """Module::Build is a system for building, testing, and installing Perl
    modules. It is meant to be an alternative to ExtUtils::MakeMaker.
    Developers may alter the behavior of the module through subclassing in a
    much more straightforward way than with MakeMaker. It also does not
    require a make on your system - most of the Module::Build code is
    pure-perl and written in a very cross-platform way.
    """

    homepage = "https://metacpan.org/pod/Module::Build"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-0.4224.tar.gz"

    version(
        "0.42.31",
        sha256="7e0f4c692c1740c1ac84ea14d7ea3d8bc798b2fb26c09877229e04f430b2b717",
        url="https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-0.4231.tar.gz",
    )
    version("0.42_30", sha256="77a185663ffcd17d7b3fc3c9b6a334f6806978b518e57b1753f35ec5e63e232c")
    version(
        "0.42.29",
        sha256="1fe491a6cda914b01bc8e592faa2b5404e9f35915ca15322f8f2a8d8f9008c18",
        url="https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-0.4229.tar.gz",
    )

    provides("perl-module-build-base")  # AUTO-CPAN2Spack
    provides("perl-module-build-compat")  # AUTO-CPAN2Spack
    provides("perl-module-build-config")  # AUTO-CPAN2Spack
    provides("perl-module-build-cookbook")  # AUTO-CPAN2Spack
    provides("perl-module-build-dumper")  # AUTO-CPAN2Spack
    provides("perl-module-build-notes")  # AUTO-CPAN2Spack
    provides("perl-module-build-ppmmaker")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-default")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-macos")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-unix")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-vms")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-vos")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-windows")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-aix")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-cygwin")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-darwin")  # AUTO-CPAN2Spack
    provides("perl-module-build-platform-os2")  # AUTO-CPAN2Spack
    provides("perl-module-build-podparser")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-parsexs@2.21:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-text-abbrev", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-tap-harness@3.29:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-perl-ostype@1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-mkbootstrap", type="run")  # AUTO-CPAN2Spack
    depends_on("perl@5.6.1:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-manifest@1.54:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-metadata@1.0.2:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-cpan-meta-yaml@0.3:", type=("build", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-data-dumper", type="run")  # AUTO-CPAN2Spack
