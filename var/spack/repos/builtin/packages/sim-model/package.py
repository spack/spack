# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from llnl.util import tty

from contextlib import contextmanager
import os
import shutil


class SimModel(Package):
    """The abstract base package for simulation models.

    Simulation models are groups of nmodl mechanisms. These packages are
    deployed as neuron/coreneuron modules (dynamic loadable libraries)
    which are loadable using load_dll() or linked into a "special"

    Specific models packages can be added to spack by simply inheriting from
    this class and defining basic attributes, e.g.:
    ```
    class ModelHippocampus(SimModel):
        homepage = ""
        git = "ssh://bbpcode.epfl.ch/sim/models/hippocampus"
        version('develop', branch='master')
    ```

    Nevertheless, for them to become full neurodamus packages, they may inherit from
    NeurodamusModel instead. See neurodamus-xxx packages for examples.

    """
    variant('coreneuron',  default=False, description="Enable CoreNEURON Support")
    variant('profile',     default=False, description="Enable profiling using Tau")

    # neuron/corenrn get linked automatically when using nrnivmodl[-core]
    # Dont duplicate the link dependency (only 'build' and 'run')
    depends_on('neuron+mpi', type=('build', 'run'))
    depends_on('coreneuron', when='+coreneuron', type=('build', 'run'))
    depends_on('neuron+profile', when='+profile', type=('build', 'run'))
    depends_on('coreneuron+profile', when='+coreneuron+profile', type=('build', 'run'))
    depends_on('tau', when='+profile')

    conflicts('^neuron~python', when='+coreneuron')

    phases = ('build', 'install')

    mech_name = None
    """The name of the mechanism, defined in subclasses"""

    def build(self, spec, prefix):
        """Build phase"""
        self._build_mods('mod')

    @property
    def lib_suffix(self):
        return ('_' + self.mech_name) if self.mech_name else ''

    def _build_mods(self, mods_location, link_flag='', include_flag='', corenrn_mods=None,
                    dependencies=None):
        """Build shared lib & special from mods in a given path
        """
        # pass include and link flags for all dependency libraries
        # Compiler wrappers are not used to have a more reproducible building
        if dependencies is None:
            dependencies = self.spec.dependencies_dict('link').keys()
        for dep in set(dependencies):
            link_flag += " {0.ld_flags} {0.rpath_flags}".format(self.spec[dep].libs)
            include_flag += " -I " + str(self.spec[dep].prefix.include)

        include_flag += ' -DENABLE_TAU_PROFILER' if '+profile' in self.spec else ''
        output_dir = os.path.basename(self.neuron_archdir)

        if self.spec.satisfies('+coreneuron'):
            libnrncoremech = self.__build_mods_coreneuron(
                corenrn_mods or mods_location, link_flag, include_flag
            )
            # Relevant flags to build neuron's nrnmech lib
            include_flag += ' -DENABLE_CORENEURON'  # only now, otherwise mods assume neuron
            include_flag += ' -I%s' % self.spec['coreneuron'].prefix.include
            link_flag += ' ' + libnrncoremech.ld_flags

        # Neuron mechlib and special
        with profiling_wrapper_on():
            link_flag += ' -L{0} -Wl,-rpath,{0}'.format(str(self.prefix.lib))
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, mods_location)

        assert os.path.isfile(os.path.join(output_dir, 'special'))
        return include_flag, link_flag

    def __build_mods_coreneuron(self, mods_location, link_flag, include_flag):
        mods_location = os.path.abspath(mods_location)
        assert os.path.isdir(mods_location) and find(mods_location, '*.mod', recursive=False),\
            'Invalid mods dir: ' + mods_location
        nrnivmodl_params = ['-n', self.mech_name,
                            '-i', include_flag,
                            '-l', link_flag,
                            '-V',
                            'mod']
        with working_dir('build_' + self.mech_name, create=True):
            force_symlink(mods_location, 'mod')
            which('nrnivmodl-core')(*nrnivmodl_params)
            output_dir = os.path.basename(self.neuron_archdir)
            mechlib = find_libraries('libcorenrnmech' + self.lib_suffix + '*', output_dir)
            assert len(mechlib.names) == 1, 'Error creating corenrnmech. Found: ' + str(mechlib.names)
        return mechlib

    def install(self, spec, prefix, install_src=True):
        """Install phase

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        """
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.share.modc)

        self._install_binaries()

        if install_src:
            self._install_src(prefix)

    def _install_binaries(self, mech_name=None):
        # Install special
        mech_name = mech_name or self.mech_name
        arch = os.path.basename(self.neuron_archdir)
        prefix = self.prefix

        if self.spec.satisfies('+coreneuron'):
            with working_dir('build_' + mech_name):
                if self.spec.satisfies('^coreneuron@0.0:0.14'):
                    raise Exception('Coreneuron versions before 0.14 are not supported by Neurodamus model')
                elif self.spec.satisfies('^coreneuron@0.14:0.16.99'):
                    which('nrnivmech_install.sh', path=".")(prefix)
                else:
                    which('nrnivmodl-core')("-d", prefix, 'mod')  # Set dest to install

        # Install special
        shutil.copy(join_path(arch, 'special'), prefix.bin)

        if self.spec.satisfies('^neuron~binary'):
            # Install libnrnmech - might have several links.
            for f in find(arch + '/.libs', 'libnrnmech*.so*', recursive=False):
                if not os.path.islink(f):
                    bname = os.path.basename(f)
                    lib_dst = prefix.lib.join(bname[:bname.find('.')] + self.lib_suffix + '.so')
                    shutil.move(f, lib_dst)  # Move so its not copied twice
                    break
            else:
                raise Exception('No libnrnmech found')

            # Patch special for the new libname
            which('sed')('-i.bak',
                         's#-dll .*#-dll %s "$@"#' % lib_dst,
                         prefix.bin.special)
            os.remove(prefix.bin.join('special.bak'))

    def _install_src(self, prefix):
        """Copy original and translated c mods
        """
        arch = os.path.basename(self.neuron_archdir)
        mkdirp(prefix.lib.mod, prefix.lib.hoc, prefix.lib.python)
        copy_all('mod', prefix.lib.mod)
        copy_all('hoc', prefix.lib.hoc)
        if os.path.isdir('python'):  # Recent neurodamus
            copy_all('python', prefix.lib.python)

        for cmod in find(arch, '*.c', recursive=False):
            shutil.move(cmod, prefix.share.modc)

    def _setup_environment_common(self, spack_env, run_env):
        spack_env.unset('LC_ALL')
        # Dont export /lib as an ldpath. We dont want to find these libs automatically
        to_rm = ('LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'DYLD_FALLBACK_LIBRARY_PATH')
        run_env.env_modifications = [envmod for envmod in run_env.env_modifications
                                     if envmod.name not in to_rm]
        if os.path.isdir(self.prefix.lib.hoc):
            run_env.prepend_path('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        if os.path.isdir(self.prefix.lib.python):
            run_env.prepend_path('PYTHONPATH', self.prefix.lib.python)

    def setup_environment(self, spack_env, run_env):
        self._setup_environment_common(spack_env, run_env)
        # We will find 0 or 1 lib
        for libnrnmech_name in find(self.prefix.lib, 'libnrnmech*.so', recursive=False):
            run_env.prepend_path('BGLIBPY_MOD_LIBRARY_PATH', libnrnmech_name)


@contextmanager
def profiling_wrapper_on():
    os.environ['USE_PROFILER_WRAPPER'] = '1'
    yield
    del os.environ['USE_PROFILER_WRAPPER']
