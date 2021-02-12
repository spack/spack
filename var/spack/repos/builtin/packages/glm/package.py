# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glm(CMakePackage):
    """OpenGL Mathematics (GLM) is a header only C++ mathematics library for
    graphics software based on the OpenGL Shading Language (GLSL) specification
    """

    homepage = "https://github.com/g-truc/glm"
    url = "https://github.com/g-truc/glm/archive/0.9.7.1.tar.gz"

    version('0.9.9.8', sha256='7d508ab72cb5d43227a3711420f06ff99b0a0cb63ee2f93631b162bfe1fe9592')
    version('0.9.9.7', sha256='2ec9e33a80b548892af64fbd84a947f93f0e725423b1b7bec600f808057a8239')
    version('0.9.9.6', sha256='30b05f31f5d8528caa9fc8fe8132e5a0444d55b1c39db53fe4db8857654afafc')
    version('0.9.9.5', sha256='5e33b6131cea6a904339734b015110d4342b7dc02d995164fdb86332d28a5aa4')
    version('0.9.9.4', sha256='3a073eb8f3be07cee74481db0e1f78eda553b554941e405c863ab64de6a2e954')
    version('0.9.9.3', sha256='fba9fd177073a36c5a7798c74b28e79ba6deb8f4bb0d2dbfc0e207c27da7e12c')
    version('0.9.9.2', sha256='39ed8d2fff3de053c98f1381dccfa9cee524a89c5b00d204d58dec56cf4ffb33')
    version('0.9.9.1', sha256='88220450f447676b36ff34ae3db5a435accf04c4bfed8808402cac69918cee91')
    version('0.9.9.0', sha256='514dea9ac0099dc389cf293cf1ab3d97aff080abad55bf79d4ab7ff6895ee69c')
    version('0.9.7.1', sha256='285a0dc8f762b4e523c8710fbd97accaace0c61f45bc8be2bdb0deed07b0e6f3')

    depends_on('cmake@2.6:', type='build')
