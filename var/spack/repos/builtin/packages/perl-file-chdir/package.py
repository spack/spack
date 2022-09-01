# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileChdir(PerlPackage):
    """Perl's chdir() has the unfortunate problem of being very, very, very
    global. If any part of your program calls chdir() or if any library you use
    calls chdir(), it changes the current working directory for the *whole*
    program.

    This sucks.

    File::chdir gives you an alternative, $CWD and @CWD. These two variables
    combine all the power of chdir(), File::Spec and Cwd."""

    homepage = "https://metacpan.org/pod/File::chdir"
    url = "https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/File-chdir-0.1011.tar.gz"

    version(
        "0.10.11",
        sha256="31ebf912df48d5d681def74b9880d78b1f3aca4351a0ed1fe3570b8e03af6c79",
        url="https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/File-chdir-0.1011.tar.gz",
    )
    version(
        "0.10.10",
        sha256="efc121f40bd7a0f62f8ec9b8bc70f7f5409d81cd705e37008596c8efc4452b01",
        url="https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/File-chdir-0.1010.tar.gz",
    )
