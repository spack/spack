# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestWarnings(PerlPackage):
    """Test for warnings and the lack of them"""

    homepage = "http://deps.cpantesters.org/?module=Test%3A%3ACleanNamespaces;perl=latest"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Warnings-0.026.tar.gz"

    version("0.031", sha256="1e542909fef305e45563e9878ea1c3b0c7cef1b28bb7ae07eba2e1efabec477b")
    version("0.030", sha256="89a4947ddf1564ae01122275584433d7f6c4370370bcf3768922d796956ae24f")
    version("0.029", sha256="b55214ea50395f1ae14ac504dd3d0d21580a92c558e8049cbe7b3ac42add1792")
    version("0.028", sha256="26fda9f8d279e943d27e43a4a3a5cea8a6592cd36e7308695f8dc6602262c0e0")
    version("0.027", sha256="118dd9f48408557555f0af5478e0e873f9df0952cf5911f697a4ce5165880864")
    version("0.026", sha256="ae2b68b1b5616704598ce07f5118efe42dc4605834453b7b2be14e26f9cc9a08")
    depends_on("perl@5.6:", type=("build", "run", "test"))  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type=("build", "test"))  # AUTO-CPAN2Spack
