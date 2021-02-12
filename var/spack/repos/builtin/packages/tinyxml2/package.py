# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tinyxml2(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml2/"
    url = "https://github.com/leethomason/tinyxml2/archive/3.0.0.tar.gz"

    version('8.0.0', sha256='6ce574fbb46751842d23089485ae73d3db12c1b6639cda7721bf3a7ee862012c')
    version('7.1.0', sha256='68ebd396a4220d5a9b5a621c6e9c66349c5cfdf5efaea3f16e3bb92e45f4e2a3')
    version('7.0.1', sha256='a381729e32b6c2916a23544c04f342682d38b3f6e6c0cad3c25e900c3a7ef1a6')
    version('7.0.0', sha256='fa0d1c745d65d4d833e62cb183e23c2034dc7a35ec1a4977e808bdebb9b4fe60')
    version('6.2.0', sha256='cdf0c2179ae7a7931dba52463741cf59024198bbf9673bf08415bcb46344110f')
    version('6.0.0', sha256='9444ba6322267110b4aca61cbe37d5dcab040344b5c97d0b36c119aa61319b0f')
    version('5.0.1', sha256='cd33f70a856b681506e3650f9f5f5e5e6c7232da7fa3cfc4e8f56fe7b77dd735')
    version('5.0.0', sha256='d88cd8cece80162a2d7a1a0801aa4fc771d4ed6b094b475d00f303eda30bc87d')
    version('4.0.1', sha256='14b38ef25cc136d71339ceeafb4856bb638d486614103453eccd323849267f20')
    version('4.0.0', sha256='90add44f06de081047d431c08d7269c25b4030e5fe19c3bc8381c001ce8f258c')
    version('3.0.0', sha256='128aa1553e88403833e0cccf1b651f45ce87bc207871f53fdcc8e7f9ec795747')
    version('2.2.0', sha256='f891224f32e7a06bf279290619cec80cc8ddc335c13696872195ffb87f5bce67')
    version('2.1.0', sha256='4bdd6569fdce00460bf9cda0ff5dcff46d342b4595900d849cc46a277a74cce6')
    version('2.0.2', sha256='3cc3aa09cd1ce77736f23488c7cb24e65e11daed4e870ddc8d352aa4070c7c74')
