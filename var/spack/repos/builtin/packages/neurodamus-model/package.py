# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from contextlib import contextmanager
import shutil
import os


class NeurodamusModel(Package):
    """An 'abstract' base package for Simulation Models. Therefore no version.
       Eventually in the future Models are independent entities, not tied to neurodamus
    """
    variant('coreneuron',  default=False, description="Enable CoreNEURON Support")
    variant('profile',     default=False, description="Enable profiling using Tau")
    variant('synapsetool', default=True,  description="Enable Synapsetool reader")
    variant('sonata',      default=False, description="Enable Synapsetool with Sonata")
    variant('python',      default=False, description="Install neurodamus-python alongside")

    depends_on('neurodamus-core')
    depends_on('neurodamus-core+python', when='+python')

    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("neuron+mpi")
    depends_on('reportinglib')
    depends_on('coreneuron', when='+coreneuron')
    depends_on('synapsetool+mpi', when='+synapsetool~sonata')
    depends_on('synapsetool+mpi+sonata', when='+synapsetool+sonata')

    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static, and we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    depends_on('neuron+profile', when='+profile')
    depends_on('coreneuron+profile', when='+coreneuron+profile')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('tau', when='+profile')

    conflicts('^neuron~python', when='+coreneuron')
    conflicts('+sonata', when='~synapsetool')

    # ---
    phases = ['merge_hoc_mod', 'build', 'install']

    # These vars can be overriden by subclasses to specify additional sources
    # This is required since some models may have a different source structure
    _hoc_srcs = ('hoc',)
    _mod_srcs = ('mod',)

    # The name of the mechanism, which cen be overriden
    mech_name = ''

    def merge_hoc_mod(self, spec, prefix):
        core_prefix = spec['neurodamus-core'].prefix
        merged_hoc = '_merged_hoc'
        merged_mod = '_merged_mod'
        merged_mod_core = '_core_mechs'

        # First Initialize with core hoc / mods
        copy_tree(core_prefix.hoc, merged_hoc)
        copy_tree(core_prefix.mod, merged_mod)

        # If we shall build mods for coreneuron, only bring from core those specified
        if spec.satisfies("+coreneuron"):
            mkdirp(merged_mod_core)
            with open(core_prefix.mod.join("coreneuron_modlist.txt")) as core_mods:
                for aux_mod in core_mods:
                    shutil.copy(core_prefix.mod.join(aux_mod.strip()), merged_mod_core)

        # Copy from the several sources (typically just 'hoc' and 'mod')
        for hoc_src in self._hoc_srcs:
            copy_all(hoc_src, merged_hoc)
        for mod_src in self._mod_srcs:
            copy_all(mod_src, merged_mod)
            if spec.satisfies("+coreneuron"):
                copy_all(mod_src, merged_mod_core)

    def build(self, spec, prefix):
        """ Build mod files from m dir with nrnivmodl
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        force_symlink('_merged_mod', 'm')
        dep_libs = ['reportinglib', 'hdf5',  'zlib']

        profile_flag = '-DENABLE_TAU_PROFILER' if '+profile' in spec else ''
        link_flag = '-Wl,-rpath,' + prefix.lib
        include_flag = ' -I%s -I%s %s' % (spec['reportinglib'].prefix.include,
                                          spec['hdf5'].prefix.include,
                                          profile_flag)
        if '+synapsetool' in spec:
            include_flag += ' -DENABLE_SYNTOOL -I ' + spec['synapsetool'].prefix.include
            dep_libs.append('synapsetool')

        for dep in dep_libs:
            link_flag += self._get_lib_flags(dep)

        # If synapsetool is static we have to bring dependencies
        if spec.satisfies('+synapsetool') and spec['synapsetool'].satisfies('~shared'):
            link_flag += ' ' + spec['synapsetool'].package.dependency_libs(spec).joined()

        # Create corenrn mods
        if '+coreneuron' in spec:
            include_flag += ' -I%s' % (spec['coreneuron'].prefix.include)
            which('nrnivmodl-core')(
                '-i', include_flag, '-l', link_flag, '-n', self.mech_name,
                '-v', str(spec.version), '-c', '_core_mechs')
            output_dir = spec.architecture.target
            mechlib = find_libraries("libcorenrnmech*", output_dir)
            assert len(mechlib), "Error creating corenrnmech lib"

            # Link neuron special with this mechs lib
            link_flag += ' ' + mechlib.ld_flags + self._get_lib_flags('coreneuron')
            include_flag += ' -DENABLE_CORENEURON'  # only now, otherwise some mods assume neuron

        with profiling_wrapper_on():
            which('nrnivmodl')('-incflags', include_flag, '-loadflags', link_flag, 'm')
        special = os.path.join(os.path.basename(self.neuron_archdir), 'special')
        assert os.path.isfile(special)

    def _get_lib_flags(self, lib_name):
        """ Helper method to get linking flags similar to spack build, for solid deployments:
              1. static libs passed via full path
              2. shared libs passed with -L -l and RPATH flags
            Attention: This func doesnt handle recursive deps of static libs.
        """
        spec = self.spec[lib_name]
        if spec.satisfies('+shared'):  # Prefer shared if both exist
            return " %s %s" % (spec.libs.rpath_flags, spec.libs.ld_flags)
        return ' ' + spec.libs.joined()

    def install(self, spec, prefix):
        """ Install:
              bin/ <- special and special-core
              lib/ <- hoc, mod and lib*mech*.so
              share/ <- neuron & coreneuron mod.c's (modc and modc_core)
              python/ If neurodamus-core comes with python, create links
        """
        mkdirp(prefix.bin)
        mkdirp(prefix.lib)
        mkdirp(prefix.share.modc)
        shutil.move('_merged_hoc', prefix.lib.hoc)
        shutil.move('_merged_mod', prefix.lib.mod)

        arch = os.path.basename(self.neuron_archdir)
        shutil.move(join_path(arch, 'special'), prefix.bin)

        # Copy c mods (for neuron)
        for cmod in find(arch, "*.c", recursive=False):
            shutil.move(cmod, prefix.share.modc)

        # Handle non-binary special
        if os.path.exists(arch + "/.libs/libnrnmech.so"):
            shutil.move(arch + "/.libs/libnrnmech.so", prefix.lib)
            sed = which('sed')
            sed('-i', 's#-dll .*#-dll %s#' % prefix.lib.join('libnrnmech.so'),
                prefix.bin.special)

        if spec.satisfies('+coreneuron'):
            outdir = spec.architecture.target
            install = which('nrnivmech_install.sh', path=".")
            install(prefix)
            # Then modc
            shutil.move(join_path(outdir, 'core/mod2c'), prefix.share.modc_core)

        if spec.satisfies('+python'):
            py_src = spec['neurodamus-core'].prefix.python
            assert os.path.isdir(py_src)
            # Link required paths, create a new lib link (to our lib)
            py_dst = prefix.lib.python
            mkdirp(py_dst)
            force_symlink('../lib', py_dst.lib)
            for name in ('neurodamus', 'init.py', '_debug.py'):
                force_symlink(py_src.join(name), py_dst.join(name))

    def setup_environment(self, spack_env, run_env):
        spack_env.unset('LC_ALL')
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


# Aux funcs
# ---------
def copy_all(src, dst, copyfunc=shutil.copy):
    """Copies/processes all files in a src dir against a destination dir"""
    isdir = os.path.isdir
    for name in os.listdir(src):
        pth = join_path(src, name)
        isdir(pth) or copyfunc(pth, dst)


def symlink2(src, dst):
    """Simple alternative to symlink, copy compat"""
    if os.path.isdir(dst):
        dst_dir = dst
        dst = join_path(dst, os.path.basename(src))
    else:
        dst_dir = os.path.dirname(dst)
    src = os.path.relpath(src, dst_dir)  # update path relation
    # Silently replace links, just like copy replaces files
    if os.path.islink(dst):
        os.remove(dst)
    os.symlink(src, dst)


def filter_out(src, dst):
    """Remove src from dst, copy compat"""
    fname = join_path(dst, os.path.basename(src))
    if os.path.exists(fname):
        os.remove(fname)


# Shortcut to extra operators
copy_all.symlink2 = symlink2
copy_all.filter_out = filter_out
