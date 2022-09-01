# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect

from spack.package import *
from spack.util.executable import Executable


class _WrappedExecutable(Executable):
    def __init__(self, executable):
        super(_WrappedExecutable, self).__init__(executable.path)

    def __call__(self, *args, **kwargs):
        spack_answers_filename = "common_sense_answer.txt"
        with open(spack_answers_filename, "w") as f:
            f.writelines("y\n")
        with open(spack_answers_filename, "r") as f:
            super(_WrappedExecutable, self).__call__(*args, **kwargs, input=f)


class PerlJsonXs(PerlPackage):
    """JSON serialising/deserialising, done correctly and fast."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-4.03.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("4.03", sha256="515536f45f2fa1a7e88c8824533758d0121d267ab9cb453a1b5887c8a56b9068")
    version("4.02", sha256="a5ad172138071a14729da8a01921ca233da4fe2bed290ffdfb8e560dd8adcf16")

    depends_on("perl-canary-stability", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-common-sense", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker@6.52:", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-types-serialiser", type="run")  # AUTO-CPAN2Spack

    def configure(self, spec, prefix):
        perl_safe = inspect.getmodule(self).perl
        inspect.getmodule(self).perl = _WrappedExecutable(perl_safe)

        try:
            super(PerlJsonXs, self).configure(spec, prefix)
        finally:
            inspect.getmodule(self).perl = perl_safe
