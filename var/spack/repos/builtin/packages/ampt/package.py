# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ampt(MakefilePackage):
    """A Multi-Phase Transport (AMPT) model is a Monte Carlo transport model for
       nuclear collisions at relativistic energies."""

    homepage = "http://myweb.ecu.edu/linz/ampt/"
    url      = "http://myweb.ecu.edu/linz/ampt/ampt-v1.26t9b-v2.26t9b.zip"

    maintainers = ['vvolkl']

    tags = ['hep']

    version('v2.26t9', sha256='d90e2e5a88f93baec69bc56d67ed8e35dc243fd1e5104e551e8d7e69fd09716a')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share.ampt)
        install('ampt', prefix.bin)
        install('input.ampt', prefix.share.ampt)
        install('readme', prefix.share.ampt)
