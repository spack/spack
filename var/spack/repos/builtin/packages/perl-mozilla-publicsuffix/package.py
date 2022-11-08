# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from llnl.util.filesystem import filter_file

from spack.package import *


class PerlMozillaPublicsuffix(PerlPackage):
    """Get a domain name's public suffix via the Mozilla Public Suffix List."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/T/TO/TOMHUKINS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/T/TO/TOMHUKINS/Mozilla-PublicSuffix-v1.0.6.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.0.6", sha256="a3bc115d6a59fb7bf23b539fb7b95e4ee06850fab884e2d12dd98dc545f9ebd8")
    version("1.0.5", sha256="2750fca9335025eaf228a69952dd41a5d361a06b6baca7169865f8de510f3848")

    depends_on("perl-module-build", type="build")

    depends_on("perl@5.8:", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-uri", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-module-build@0.28:", type="build")  # AUTO-CPAN2Spack

    def patch(self):
        """HTTP::Tiny has a bad interaction with Errno.pm for Perl <5.22"""
        filter_file(r"^use HTTP::Tiny;$", "", "Build.PL", stop_at="^my", backup=False)


class PerlBuilder(spack.build_systems.perl.PerlBuilder):
    class _WrappedExecutable(Executable):
        def __init__(self, executable):
            super(PerlBuilder._WrappedExecutable, self).__init__(executable.path)

        def __call__(self, *args, **kwargs):
            config_answers = ["N\n"]
            config_answers_filename = "spack-config.in"

            with open(config_answers_filename, "w") as f:
                f.writelines(config_answers)

            with open(config_answers_filename, "r") as f:
                super(PerlBuilder._WrappedExecutable, self).__call__(*args, **kwargs, input=f)

    def configure(self, pkg, spec, prefix):
        perl_safe = inspect.getmodule(self).perl
        inspect.getmodule(self).perl = PerlBuilder._WrappedExecutable(perl_safe)

        try:
            super(PerlBuilder, self).configure(pkg, spec, prefix)
        finally:
            inspect.getmodule(self).perl = perl_safe
