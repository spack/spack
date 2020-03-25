# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4emlow(Package):
    """Geant4 data files for low energy electromagnetic processes."""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4EMLOW.6.50.tar.gz"
    maintainers = ['drbenmorgan']

    version(
        '6.50', sha256='c97be73fece5fb4f73c43e11c146b43f651c6991edd0edf8619c9452f8ab1236')
    version(
        '7.3', sha256='583aa7f34f67b09db7d566f904c54b21e95a9ac05b60e2bfb794efb569dba14e')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4EMLOW{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4.web.cern.ch/support/source/G4EMLOW.%s.tar.gz" % version)
