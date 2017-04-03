import os
import shutil
from spack import *

class Rockstar(Package):
    """Description"""

    homepage = "https://bitbucket.org/gfcstanford/rockstar"
    url      = "https://bitbucket.org/gfcstanford/rockstar"

    version('develop', git='https://bitbucket.org/gfcstanford/rockstar.git')
    version('yt', hg='https://bitbucket.org/MatthewTurk/rockstar')

    variant('hdf5', description='Build rockstar with HDF5 support')

    patch('adjust_buildscript.patch')

    depends_on('hdf5', when='+hdf5')

    def install(self, spec, prefix):
        # Set environment appropriately for HDF5
        if '+hdf5' in spec:
            os.environ['HDF5_INC_DIR'] = spec.get_dependency('hdf5').spec.prefix+"/include"
            os.environ['HDF5_LIB_DIR'] = spec.get_dependency('hdf5').spec.prefix+"/lib"

	# Build depending on whether hdf5 is to be used
        if '+hdf5' in spec:
            make('with_hdf5')
        else:
            make()

	# Build rockstar library
        make('lib')

        # Install all files and directories
        for filename in os.listdir('.'):
            if filename != "." and filename != "..":
                if os.path.isdir(filename):
                    shutil.copytree(join_path(".",filename), join_path(prefix, filename))
                else:
                    install(filename, join_path(prefix, filename))
