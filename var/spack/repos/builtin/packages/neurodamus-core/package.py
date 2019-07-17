# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
import os
import shutil
import llnl.util.tty as tty


class NeurodamusCore(Package):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"

    version('develop', git=git, branch='master', clean=False)
    version('2.4.3', git=git, tag='2.4.3', clean=False)
    version('2.4.1', git=git, tag='2.4.1', clean=False)
    version('2.3.4', git=git, tag='2.3.4', clean=False)
    version('2.3.3', git=git, tag='2.3.3', clean=False)
    version('2.2.1', git=git, tag='2.2.1', clean=False)

    variant('python', default=False, description="Enable Python Neurodamus")
    variant('common', default=False, description="Merge in synapse mechanisms hoc & mods")

    # Attempt to support building
    depends_on('neuron~binary+python~mpi', when='+common')

    # Neurodamus py is currently an extension to core
    resource(name='pydamus',
             git='ssh://bbpcode.epfl.ch/sim/neurodamus-py',
             when='+python',
             destination='resources')

    resource(name='common',
             git='ssh://bbpcode.epfl.ch/sim/models/common',
             when='+common',
             destination='resources')

    depends_on('python@2.7:',      type=('build', 'run'), when='+python')
    depends_on('py-setuptools',    type=('build', 'run',), when='+python')
    depends_on('py-h5py',          type=('run',), when='+python')
    depends_on('py-numpy',         type=('run',), when='+python')
    depends_on('py-enum34',        type=('run',), when='^python@2.4:2.7.999,3.1:3.3.999')
    depends_on('py-lazy-property', type=('run'), when='+python')

    def install(self, spec, prefix):
        shutil.copytree('hoc', prefix.hoc)
        shutil.copytree('mod', prefix.mod)
        if spec.satisfies('+python'):
            copy_tree('resources/neurodamus-py', prefix.python)

        filter_file(r'UNKNOWN_CORE_VERSION', r'%s' % spec.version, prefix.hoc.join('defvar.hoc'))
        try:
            commit_hash = self.fetcher[0].get_commit()
            filter_file(r'UNKNOWN_CORE_HASH', r'\'%s\'' % commit_hash, prefix.hoc.join('defvar.hoc'))
        except Exception as e:
            tty.warn(str(e))

        # +Common will bring common mods and build a bare nrnmechlib
        if spec.satisfies('+common'):
            copy_all('resources/common/hoc', prefix.hoc)
            copy_all('resources/common/mod', prefix.mod)

            # However it brings some files that require Mpi and we must avoid them
            for f in ('MemUsage.mod', 'SpikeWriter.mod'):
                os.remove(prefix.mod.join(f))

            with working_dir(prefix):
                which('nrnivmodl')('-incflags', '-DDISABLE_REPORTINGLIB -DDISABLE_HDF5', 'mod')

                bindir = os.path.basename(self.neuron_archdir)
                special = join_path(bindir, 'special')
                open('.bindir', 'w').write(bindir)

                if not os.path.isfile(special):
                    raise Exception("Failed to build neurodamus core mods")

                # Cleanup
                for f in find(bindir, '*.lo'): os.remove(f)
                for f in find(bindir, '*.mod'): os.remove(f)
                for f in find(bindir + '/.libs', '*.o'): os.remove(f)
                os.mkdir(bindir + "/modc")
                for f in find(bindir, "*.c*"): shutil.move(f, bindir + "/modc/")

    def setup_environment(self, spack_env, run_env):
        run_env.set('HOC_LIBRARY_PATH', self.prefix.hoc)
        if self.spec.satisfies('+common'):
            run_env.set('MOD_LIBRARY_PATH', self.prefix.mod)
            bindir_info = self.prefix.join('.bindir')
            if os.path.isfile(bindir_info):
                bindir = open(bindir_info, 'r').readline()
                mechlib = find_libraries('libnrnmech', join_path(self.prefix, bindir, '.libs'))[0]
                run_env.set('NRNMECH_LIB_PATH', mechlib)
            else:
                tty.warn("No .bindir info file found. NRNMECH_LIB_PATH env var wont be set")
