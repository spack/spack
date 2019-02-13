from spack import *
import os


class G4nucleonxs(Package):
    """Geant4 data from evaluated cross-sections in SAID data-base """
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.1.1.tar.gz"

    version('1.1', 'a38cd9a83db62311922850fe609ecd250d36adf264a88e88c82ba82b7da0ed7f')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.set('G4SAIDDATA', join_path(prefix.share, 'data'))
        run_env.set('G4SAIDXSDATA', join_path(prefix.share, 'data'))

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.%s.tar.gz" % version
