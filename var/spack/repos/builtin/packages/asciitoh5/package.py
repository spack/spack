##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil
import os


class Asciitoh5(Package):
    """Neurodamus Library necessary to convert from ASCII to H5"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/asciitoh5.git"
    git      = "git@bbpgitlab.epfl.ch:hpc/asciitoh5.git"

    version('develop', git=git, branch='master')
    version('1.0', git=git, tag='1.0')

    depends_on('neuron')
    depends_on('hdf5')

    def install(self, spec, prefix):
        os.mkdir(prefix.lib)
        shutil.copytree('hoc', prefix.lib.hoc)
        shutil.copytree('mod', prefix.lib.mod)
        shutil.copytree('bin', prefix.bin)
        with working_dir(prefix):
            libs = spec['hdf5'].libs
            link_flag = ''.join([
                ' '.join(['-Wl,-rpath,' + x for x in libs.directories]),
                libs.ld_flags
            ])
            include_flag = ' -I%s' % (spec['hdf5'].prefix.include)
            which('nrnivmodl')('-incflags', include_flag, '-loadflags',
                               link_flag, 'lib/mod')
            archdir = os.path.basename(self.nrnivmodl_outdir)
            src = join_path(prefix, archdir, 'special')
            dest = join_path(prefix.bin, 'special')
            symlink(src, dest)

    def setup_run_environment(self, env):
        env.set('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        env.set('NEURON_INIT_MPI', "0")
        env.unset('PMI_RANK')
