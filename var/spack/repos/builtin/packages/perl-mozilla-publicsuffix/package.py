# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack.package import *


class _WrappedExecutable(Executable):
    def __init__(self, executable):
        super(_WrappedExecutable, self).__init__(executable.path)

    def __call__(self, *args, **kwargs):
        spack_answers_filename = "common_sense_answer.txt"
        with open(spack_answers_filename, "w") as f:
            f.writelines("n\n")
        with open(spack_answers_filename, "r") as f:
            super(_WrappedExecutable, self).__call__(*args, **kwargs, input=f)


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

    def configure(self, spec, prefix):
        perl_safe = inspect.getmodule(self).perl
        inspect.getmodule(self).perl = _WrappedExecutable(perl_safe)

        try:
            super(PerlMozillaPublicsuffix, self).configure(spec, prefix)
        finally:
            inspect.getmodule(self).perl = perl_safe
