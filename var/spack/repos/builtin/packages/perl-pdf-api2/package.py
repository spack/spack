# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlPdfApi2(PerlPackage):
    """Facilitates the creation and modification of PDF files"""

    homepage = "http://search.cpan.org/~ssimms/PDF-API2-2.033/lib/PDF/API2.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/S/SS/SSIMMS/PDF-API2-2.033.tar.gz"

    version('2.038', sha256='7447c4749b02a784f525d3c7ece99d34b0a10475db65096f6316748dd2f9bd09')
    version('2.037', sha256='142803d1886d2a2919d374fb6c25681630aa26740e3f8023337f996fa6c6297e')
    version('2.036', sha256='070444e9fef8beb6f115994a6ac89533fe8ba02d5e240a35bb07adcbcb511774')
    version('2.035', sha256='7e4435ff51c808451f53fa161672ba2eaa7c4d49f4ab6506801383882405bf80')
    version('2.034', sha256='8aa98818fb6e4bebd6f9096e222989dcdd5fd4c5fa2ad1c7f0149053fc68f1cc')
    version('2.033', sha256='9c0866ec1a3053f73afaca5f5cdbe6925903b4ce606f4bf4ac317731a69d27a0')

    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-test-memory-cycle', type=('build', 'run'))
    depends_on('perl-font-ttf', type=('build', 'run'))
