# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Vcsh(Package):
    """config manager based on git"""
    homepage = "https://github.com/RichiH/vcsh"
    url      = "https://github.com/RichiH/vcsh/archive/v1.20151229.tar.gz"

    version('1.20151229-1', '85c18fb15e5837d417b22980683e69ed')
    version('1.20151229', '61edf032807bba98c41c62bb2bd3d497')
    version('1.20150502', 'a6c75b5754e04bd74ae701967bb38e19')
    version('1.20141026', 'e8f42a9dbb7460f641545bea5ca1cbc4')
    version('1.20141025', '93c7fad67ab4300d76d753a32c300831')

    depends_on('git', type='run')

    # vcsh provides a makefile, if needed the install method should be adapted
    def install(self, spec, prefix):
        install('vcsh', prefix.bin)
