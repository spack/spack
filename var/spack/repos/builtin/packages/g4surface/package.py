# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class G4surface(Package):
    """Geant4 data for measured optical surface reflectance"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/RealSurface.1.0.tar.gz"

    version('1.0', '3e2d2506600d2780ed903f1f2681962e208039329347c58ba1916740679020b1')
    version('2.1', '2a287adbda1c0292571edeae2082a65b7f7bd6cf2bf088432d1d6f889426dcf3')
    version('2.1.1', '90481ff97a7c3fa792b7a2a21c9ed80a40e6be386e581a39950c844b2dd06f50')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.set('G4REALSURFACEDATA', join_path(prefix.share, 'data'))

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/RealSurface.1.0.tar.gz" % version)
