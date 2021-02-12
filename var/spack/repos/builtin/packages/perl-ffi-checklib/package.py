# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlFfiChecklib(PerlPackage):
    """This module checks whether a particular dynamic library is available for
    FFI to use. It is modeled heavily on Devel::CheckLib, but will find dynamic
    libraries even when development packages are not installed. It also
    provides a find_lib function that will return the full path to the found
    dynamic library, which can be feed directly into FFI::Platypus or another
    FFI system."""

    homepage = "https://metacpan.org/pod/FFI::CheckLib"
    url      = "https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/FFI-CheckLib-0.25.tar.gz"

    version('0.27', sha256='8d442747c24fcd8560107ed9deb98265838f17bc850cb7237f8b6d4821992d74')
    version('0.26', sha256='06e33bf0807f841626248197e8f39475ac50d1364a0336836c9b581d19a97f65')
    version('0.25', sha256='eb36b9a7cff1764a65b1b77e01e92c26207c558a3f986d0d17d2b110fa366ba4')
