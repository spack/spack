# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRlang(RPackage):
    """A toolbox for working with base types, core R features like the
       condition system, and core 'Tidyverse' features like tidy evaluation."""

    homepage = "https://cloud.r-project.org/package=rlang"
    url      = "https://cloud.r-project.org/src/contrib/rlang_0.2.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rlang"

    version('0.4.0', sha256='9748a4a217548bbe5631c18fd88c94811950446f798ff21fb327703aebaa150d')
    version('0.3.4', sha256='4e467f7b0dcbde91b60c292137d2c69cecaa713a6e4c9b7157ef6fd5453b7ade')
    version('0.3.1', sha256='30427b2be2288e88acd30c4ea348ee06043a649fd73623a63148b1ad96317151')
    version('0.3.0.1', sha256='29451db0a3cabd75761d32df47a5d43ccadbde07ecb693ffdd73f122a0b9f348')
    version('0.3.0',   sha256='9ab10ea3e19b2d60a289602ebbefa83509f430db1c8161e523896c374241b893')
    version('0.2.2', 'df2abf3a1936c503ed1edd4350ffb5f0')
    version('0.1.4', 'daed5104d557c0cbfb4a654ec8ffb579')
    version('0.1.2', '170f8cf7b61898040643515a1746a53a')
    version('0.1.1', '38a51a0b8f8487eb52b4f3d986313682')

    depends_on('r@3.1.0:', when='@:0.3.4', type=('build', 'run'))
    depends_on('r@3.2.0:', when='@0.4.0:', type=('build', 'run'))
