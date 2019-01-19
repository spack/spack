# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Singularity(AutotoolsPackage):
    """Singularity is a container platform focused on supporting 'Mobility of
       Compute'"""

    homepage = "https://www.sylabs.io/singularity/"
    url      = "https://github.com/singularityware/singularity/releases/download/2.5.2/singularity-2.5.2.tar.gz"
    git      = "https://github.com/singularityware/singularity.git"

    # Versions before 2.5.2 suffer from a serious security problem.
    # https://nvd.nist.gov/vuln/detail/CVE-2018-12021
    version('develop', branch='master')
    version('2.6.1', sha256='f38d46a225e8368eb4693137806d2dc96e925a50bdf7f6983662848831041df2')
    version('2.6.0', sha256='7c425211a099f6fa6f74037e6e17be58fb5923b0bd11aea745e48ef83c488b49')
    version('2.5.2', '2edc1a8ac9a4d7d26fba6244f1c5fd95')

    depends_on('libarchive', when='@2.5.2:')
    # these are only needed if we're grabbing the unreleased tree
    depends_on('m4',       type='build', when='@develop')
    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')

    # When installing as root, the copy has to run before chmod runs
    def install(self, spec, prefix):
        make('install', parallel=False)
