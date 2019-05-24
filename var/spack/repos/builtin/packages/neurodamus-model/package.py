# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.sim_model import SimModel
import shutil
import os


class NeurodamusModel(SimModel):
    """An 'abstract' base package for Simulation Models. Therefore no version.
       Eventually in the future Models are independent entities, not tied to neurodamus
    """
    # NOTE: Several variants / dependencies come from SimModel
    variant('synapsetool', default=True,  description="Enable Synapsetool reader")
    variant('sonata',      default=False, description="Enable Synapsetool with Sonata")
    variant('python',      default=False, description="Install neurodamus-python alongside")

    depends_on('neurodamus-core')
    depends_on('neurodamus-core+python', when='+python')

    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on('reportinglib')
    depends_on('reportinglib+profile', when='+profile')
    depends_on('synapsetool+mpi', when='+synapsetool~sonata')
    depends_on('synapsetool+mpi+sonata', when='+synapsetool+sonata')
    # NOTE: With Spack chain we no longer require support for external libs.
    # However, in some setups (notably tests) some libraries might still be
    # specificed as external and, if static, and we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    conflicts('+sonata', when='~synapsetool')

    phases = ['build_model', 'merge_hoc_mod', 'build', 'install']

    _corenrn_modlist = "coreneuron_modlist.txt"
    _lib_suffix = "_nd"

    def build_model(self, spec, prefix):
        """Build and install the bare model.
        """
        SimModel.build(self, spec, prefix)
        # Dont install intermediate src. Worse, would move mod
        SimModel.install(self, spec, prefix, install_src=False)

    def merge_hoc_mod(self, spec, prefix):
        """Add hocs and mods from neurodamus-core.

        This routine simply adds the additional mods to existing dirs
        so that incremental builds can actually happen.
        """
        core_prefix = spec['neurodamus-core'].prefix

        # If we shall build mods for coreneuron, only bring from core those specified
        if spec.satisfies("+coreneuron"):
            shutil.copytree('mod', 'mod_core', True)
            with open(core_prefix.mod.join(self._corenrn_modlist)) as core_mods:
                for aux_mod in core_mods:
                    shutil.copy(core_prefix.mod.join(aux_mod.strip()), 'mod_core')

        copy_all(core_prefix.hoc, 'hoc', make_link)
        copy_all(core_prefix.mod, 'mod', make_link)

    def build(self, spec, prefix):
        """ Build mod files from with nrnivmodl / nrnivmodl-core.
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        dep_libs = ['reportinglib', 'hdf5',  'zlib']
        link_flag = '-Wl,-rpath,' + prefix.lib
        include_flag = ' -I%s -I%s' % (spec['reportinglib'].prefix.include,
                                       spec['hdf5'].prefix.include)
        if '+synapsetool' in spec:
            include_flag += ' -DENABLE_SYNTOOL -I ' + spec['synapsetool'].prefix.include
            dep_libs.append('synapsetool')

        for dep in dep_libs:
            link_flag += ' ' + self._get_link_flags(dep)

        # If synapsetool is static we have to bring dependencies
        if spec.satisfies('+synapsetool') and spec['synapsetool'].satisfies('~shared'):
            link_flag += ' ' + spec['synapsetool'].package.dependency_libs(spec).joined()

        # Override mech_name in order to generate a library with a different name
        self.mech_name += self._lib_suffix
        self._build_mods('mod', link_flag, include_flag, 'mod_core')

        # Store flags
        self._incflags  = "-incflags '{}'\n".format(include_flag)
        self._loadflags = "-loadflags '{}'\n".format(link_flag)

    def install(self, spec, prefix):
        """Install phase.

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        python/ If neurodamus-core comes with python, create links
        """
        # base dest dirs already created by model install
        # We install binaries normally, except lib has a suffix
        self._install_binaries(lib_suffix=self._lib_suffix)

        if spec.satisfies('+coreneuron'):
            install = which('nrnivmech_install.sh', path=".")
            install(prefix)

        self._install_src(prefix)  # Will move mods. Must not happen before

        if spec.satisfies('+python'):
            py_src = spec['neurodamus-core'].prefix.python
            assert os.path.isdir(py_src)
            # Link required paths, create a new lib link (to our lib)
            py_dst = prefix.lib.python
            mkdirp(py_dst)
            force_symlink('../../lib', py_dst.lib)
            for name in ('neurodamus', 'init.py', '_debug.py'):
                force_symlink(py_src.join(name), py_dst.join(name))

    def setup_environment(self, spack_env, run_env):
        SimModel.setup_environment(self, spack_env, run_env)
        run_env.set('HOC_LIBRARY_PATH', self.prefix.lib.hoc)
        run_env.set('NEURON_INIT_MPI', "1")  # Always Init MPI (support python)

	# TODO: This is very fragile. The vars only exist if we compiled.
        if hasattr(self, '_incflags'):
            run_env.set('ND_INCFLAGS', self._incflags)
            run_env.set('ND_LOADFLAGS', self._loadflags)

        if self.spec.satisfies("+python"):
            pylib = self.prefix.lib.python
            for m in spack_env.env_modifications:
                if m.name == 'PYTHONPATH':
                    run_env.prepend_path('PYTHONPATH', m.value)
            run_env.prepend_path('PYTHONPATH', pylib)
            run_env.set('NEURODAMUS_PYTHON', pylib)

