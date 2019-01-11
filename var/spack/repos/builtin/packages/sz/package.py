# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Sz(AutotoolsPackage):
    """Error-bounded Lossy Compressor for HPC Data."""

    homepage = "https://collab.cels.anl.gov/display/ESR/SZ"
    url      = "https://github.com/disheng222/SZ/archive/v2.0.2.0.tar.gz"

    git      = "https://github.com/disheng222/SZ.git"

    version('develop', branch='master')
    version('2.0.2.0',  sha256='176c65b421bdec8e91010ffbc9c7bf7852c799972101d6b66d2a30d9702e59b0')
    version('1.4.13.5', sha256='b5e37bf3c377833eed0a7ca0471333c96cd2a82863abfc73893561aaba5f18b9')
    version('1.4.13.4', sha256='c99b95793c48469cac60e6cf82f921babf732ca8c50545a719e794886289432b')
    version('1.4.13.3', sha256='9d80390f09816bf01b7a817e07339030d596026b00179275616af55ed3c1af98')
    version('1.4.13.2', sha256='bc45329bf54876ed0f721998940855dbd5fda54379ef35dad8463325488ea4c6')
    version('1.4.13.0', sha256='baaa7fa740a47e152c319b8d7b9a69fe96b4fea5360621cdc96cb250635f946f')
    version('1.4.12.3', sha256='c1413e1c260fac7a48cb11c6dd705730525f134b9f9b244af59885d564ac7a6f')
    version('1.4.12.1', sha256='98289d75481a6e407e4027b5e23013ae83b4aed88b3f150327ea711322cd54b6')
    version('1.4.11.1', sha256='6cbc5b233a3663a166055f1874f17c96ba29aa5a496d352707ab508288baa65c')
    version('1.4.11.0', '10dee28b3503821579ce35a50e352cc6')
    version('1.4.10.0', '82e23dc5a51bcce1f70ba7e3b68a5965')
    version('1.4.9.2',  '028ce90165b7a4c4051d4c0189f193c0')

    variant('fortran', default=False,
            description='Enable fortran compilation')

    def configure_args(self):
        args = []
        if '+fortran' in self.spec:
            args += ['--enable-fortran']
        else:
            args += ['--disable-fortran']
        return args
