# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestWarnings(PerlPackage):
    """Test for warnings and the lack of them"""

    homepage = "http://deps.cpantesters.org/?module=Test%3A%3ACleanNamespaces;perl=latest"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Test-Warnings-0.026.tar.gz"

    version("0.031", sha256="1e542909fef305e45563e9878ea1c3b0c7cef1b28bb7ae07eba2e1efabec477b")
    version("0.026", sha256="ae2b68b1b5616704598ce07f5118efe42dc4605834453b7b2be14e26f9cc9a08")
