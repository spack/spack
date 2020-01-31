# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.

from spack import *
import shutil
import os

class Asciitoh5(Package):
    """Neurodamus Library necessary to convert from ASCII to H5"""

    homepage = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"
    git      = "ssh://bbpcode.epfl.ch/sim/utils/asciitoh5"

    version('develop', git=git, branch='master')
    version('1.0', git=git, tag='1.0')

    depends_on('neuron')
    depends_on('hdf5~mpi')

    def install(self, spec, prefix):
        os.mkdir(prefix.lib)
        shutil.copytree('hoc', prefix.lib.hoc)
        shutil.copytree('mod', prefix.lib.mod)
        shutil.copytree('bin', prefix.bin)
        with working_dir(prefix):
            link_flag = spec['hdf5'].libs.rpath_flags + ' ' + spec['hdf5'].libs.ld_flags
            include_flag = ' -I%s' % (spec['hdf5'].prefix.include)
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, 'lib/mod')
            bindir = os.path.basename(self.neuron_archdir)
            special = join_path(bindir, 'special')
            shutil.copy(special, prefix.bin)

    def setup_run_environment(self, env):
        env.set('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
