# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4abla(Package):
    """Geant4 data for nuclear shell effects in INCL/ABLA hadronic mode"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ABLA.3.0.tar.gz"
    maintainers = ['drbenmorgan']

    version(
        '3.0', sha256='99fd4dcc9b4949778f14ed8364088e45fa4ff3148b3ea36f9f3103241d277014')
    version(
        '3.1', sha256='7698b052b58bf1b9886beacdbd6af607adc1e099fc730ab6b21cf7f090c027ed')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4ABLA{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4ABLA.%s.tar.gz" % version)
