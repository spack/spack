from spack import *
import os


class G4nuclide(Package):
    """Geant4 data for nuclides properties"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.1.tar.gz"

    version('2.1', '933e7f99b1c70f24694d12d517dfca36d82f4e95b084c15d86756ace2a2790d9')
    version('2.2', 'dd7e27ef62070734a4a709601f5b3bada6641b111eb7069344e4f99a01d6e0a6')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.%s.tar.gz" % version
