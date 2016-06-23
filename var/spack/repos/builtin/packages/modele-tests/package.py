from spack import *

class ModeleTests(CMakePackage):
    """Tests for ModelE."""

    homepage = "https://github.com/citibeth/modele-tests"

    version('develop',
        git='git@github.com:citibeth/modele-tests.git',
        branch='develop')

    depends_on('pfunit')
    # Does not depend on ModelE; that will be provided later

    def configure_args(self):
        return []
