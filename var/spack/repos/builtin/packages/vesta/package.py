from spack import *
import os
import fnmatch
import shutil


class Vesta(Package):
    """VESTA is a 3D visualization program for structural models, volumetric data
       such as electron/nuclear densities, and crystal morphologies."""

    homepage = "http://jp-minerals.org/vesta"
    url      = "https://jp-minerals.org/vesta/archives/3.4.6/VESTA-x86_64.tar.bz2"

    version('3.4.6', '1d4651e86193f305831aa5db3dcfe789')

    depends_on('gtkplus@2.1.0:')
    depends_on('mesa')
    depends_on('cairo@1.0:')
    depends_on('gcc@5.4.0:')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix)

    def install(self, spec, prefix):
        for filename in os.listdir(self.stage.source_path):
            if os.path.isdir(filename):
                shutil.copytree(filename, join_path(self.prefix, filename))
            elif not fnmatch.fnmatch(filename, "spack-build.*"):
                shutil.copy(filename, self.prefix)
