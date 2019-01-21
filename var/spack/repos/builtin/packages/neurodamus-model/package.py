# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from contextlib import contextmanager
import shutil
import os
import sys


class NeurodamusModel(Package):
    """An 'abstract' base package for Simulation Models. Therefore no version.
       Eventually in the future Models are independent entities, not tied to neurodamus
    """
    depends_on('neurodamus-core')

    variant('coreneuron',  default=False, description="Enable CoreNEURON Support")
    variant('profile',     default=False, description="Enable profiling using Tau")
    variant('synapsetool', default=True,  description="Enable Synapsetool reader")
    variant('sonata',      default=False, description="Enable Synapsetool with Sonata")
    variant('plasticity',  default=False, description="Use optimized ProbAMPANMDA_EMS and ProbGABAAB_EMS")

    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("neuron+mpi")
    depends_on('reportinglib')
    depends_on('coreneuron', when='+coreneuron')
    depends_on('coreneuron@plasticity', when='@plasicity')
    depends_on('synapsetool+mpi', when='+synapsetool~sonata')
    depends_on('synapsetool+mpi+sonata', when='+synapsetool+sonata')

    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static, and we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    depends_on('coreneuron+profile', when='+profile')
    depends_on('neuron+profile', when='+profile')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('tau', when='+profile')

    conflicts('^neuron~python', when='+coreneuron')
    conflicts('+sonata', when='~synapsetool')

    # ---
    phases = ['merge_hoc_mod', 'build', 'install']

    # These vars can be overriden by subclasses to specify additional sources
    # This is required since some models have several sources, e.g.: thalamus
    # By default they use common (which should come from submodule)
    _hoc_srcs = ('common/hoc', 'hoc')
    _mod_srcs = ('common/mod', 'mod')

    @staticmethod
    def copy_all(src, dst, copyfunc=shutil.copy):
        isdir = os.path.isdir
        for name in os.listdir(src):
            pth = join_path(src, name)
            isdir(pth) or copyfunc(pth, dst)

    def merge_hoc_mod(self, spec, prefix):
        # First Initialize with core hoc / mods
        copy_tree(spec['neurodamus-core'].prefix.hoc, '_merged_hoc')
        copy_tree(spec['neurodamus-core'].prefix.mod, '_merged_mod')

        if spec.satisfies('+plasticity'):
            self.copy_all('common/mod/optimized', 'common/mod')

        # Copy from the several sources
        for hoc_src in self._hoc_srcs:
            self.copy_all(hoc_src, '_merged_hoc')
        for mod_src in self._mod_srcs:
            self.copy_all(mod_src, '_merged_mod')

    def build(self, spec, prefix):
        """ Build mod files from m dir with nrnivmodl
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        force_symlink('_merged_mod', 'm')
        dep_libs = ['reportinglib', 'hdf5',  'zlib']
        profile_flag = '-DENABLE_TAU_PROFILER' if '+profile' in spec else ''

        # Allow deps to not recurs bring their deps
        link_flag = '-Wl,--as-needed' if sys.platform != 'darwin' else ''
        include_flag = ' -I%s -I%s %s' % (spec['reportinglib'].prefix.include,
                                          spec['hdf5'].prefix.include,
                                          profile_flag)
        if '+synapsetool' in spec:
            include_flag += ' -DENABLE_SYNTOOL -I ' + spec['synapsetool'].prefix.include
            dep_libs.append('synapsetool')
        if '+coreneuron' in spec:
            include_flag += ' -DENABLE_CORENEURON -I%s' % (spec['coreneuron'].prefix.include)
            dep_libs.append('coreneuron')

        # link_flag. If shared use -rpath, -L, -l, otherwise lib path
        for dep in dep_libs:
            if spec[dep].satisfies('+shared'):
                link_flag += " %s %s" % (spec[dep].libs.rpath_flags, spec[dep].libs.ld_flags)
            else:
                link_flag += " " + spec[dep].libs.joined()
        if spec.satisfies('+synapsetool') and spec.satisfies('^synapsetool~shared'):
            link_flag += ' ' + spec['synapsetool'].package.dependency_libs(spec).joined()

        nrnivmodl = which('nrnivmodl')
        with profiling_wrapper_on():
            nrnivmodl('-incflags', include_flag, '-loadflags', link_flag, 'm')
        special = os.path.join(os.path.basename(self.neuron_archdir), 'special')
        assert os.path.isfile(special)

    def install(self, spec, prefix):
        """ Move hoc, mod and libnrnmech.so to lib, generated mod.c's into lib/modc.
            Find and move "special" to bin.
            If neurodamus-core comes with python, create links to it.
        """
        mkdirp(prefix.lib)
        shutil.move('_merged_hoc', prefix.lib.hoc)
        shutil.move('_merged_mod', prefix.lib.mod)
        os.makedirs(prefix.lib.modc)
        os.makedirs(prefix.bin)

        arch = os.path.basename(self.neuron_archdir)
        shutil.move(join_path(arch, 'special'), prefix.bin)

        # Copy c mods
        for cmod in find(arch, "*.c", recursive=False):
            shutil.move(cmod, prefix.lib.modc)

        # Handle non-binary special
        if os.path.exists(arch + "/.libs/libnrnmech.so"):
            shutil.move(arch + "/.libs/libnrnmech.so", prefix.lib)
            sed = which('sed')
            sed('-i', 's#-dll .*#-dll %s#' % prefix.lib.join('libnrnmech.so'),
                prefix.bin.special)

        # PY: Link only important stuff, and create a new lib link (to our lib)
        py_src = spec['neurodamus-core'].prefix.python
        if os.path.isdir(py_src):
            os.makedirs(prefix.python)
            force_symlink('../lib', prefix.python.lib)
            for name in ('neurodamus', 'init.py', '_debug.py'):
                os.symlink(py_src.join(name), prefix.python.join(name))

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('HOC_LIBRARY_PATH', self.prefix.lib.hoc)

        if os.path.isdir(self.prefix.python):
            for m in spack_env.env_modifications:
                if m.name == 'PYTHONPATH':
                    run_env.prepend_path('PYTHONPATH', m.value)
            run_env.prepend_path('PYTHONPATH', self.prefix.python)
            run_env.set('NEURODAMUS_PYTHON', self.prefix.python)

@contextmanager
def profiling_wrapper_on():
    os.environ["USE_PROFILER_WRAPPER"] = "1"
    yield
    del os.environ["USE_PROFILER_WRAPPER"]
