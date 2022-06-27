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

    patch('https://gitlab.cern.ch/sft/lcgcmake/-/raw/master/generators/patches/ampt-2.26t9b_atlas.patch',
          sha256='7a9a4f175f84dc3021301dae5d48adab1fc714fccf44ec17128a3ba1608bff4c',
          when='@2.26t9b_atlas')

    version('2.26t9b_atlas', sha256='d90e2e5a88f93baec69bc56d67ed8e35dc243fd1e5104e551e8d7e69fd09716a')
    version('2.26t9', sha256='d90e2e5a88f93baec69bc56d67ed8e35dc243fd1e5104e551e8d7e69fd09716a')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.share)
        mkdir(prefix.share.ampt)
        install('ampt', prefix.bin)
        install('input.ampt', prefix.share.ampt)
        install('readme', prefix.share.ampt)
