# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install perl-text-nsp
#
# You can edit this file again by typing:
#
#     spack edit perl-text-nsp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------
from spack.package import *


class PerlTextNsp(PerlPackage):
    """
    The Ngram Statistics Package (NSP) is a suite of programs that aids in
    analyzing Ngrams in text files.
    """

    homepage = "https://metacpan.org/dist/Text-NSP"
    url = "https://cpan.metacpan.org/authors/id/T/TP/TPEDERSE/Text-NSP-1.31.tar.gz"

    maintainers("snehring")

    version("1.31", sha256="a01201beb29636b3e41ecda2a6cf6522fd265416bd6d994fad02f59fb49cf595")
    version("1.29", sha256="26610cc17ddc3a9a239ffd100bbcf42618e2577ab4b051de4c262f2082afd27e")
