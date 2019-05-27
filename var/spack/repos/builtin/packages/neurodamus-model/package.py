# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
from spack.pkg.builtin.sim_model import SimModel
import shutil
import os

# Definitions
_CORENRN_MODLIST_FNAME = "coreneuron_modlist.txt"
_BUILD_NEURODAMUS_FNAME = "build_neurodamus.sh"
_LIB_SUFFIX = "_nd"


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
            with open(core_prefix.mod.join(_CORENRN_MODLIST_FNAME)) as core_mods:
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
        self.mech_name += _LIB_SUFFIX
        self._build_mods('mod', link_flag, include_flag, 'mod_core')

        # Create rebuild script
        with open(_BUILD_NEURODAMUS_FNAME, "w") as f:
            f.write(_BUILD_NEURODAMUS_TPL.format(nrnivmodl=str(which('nrnivmodl')),
                                                 incflags=include_flag,
                                                 loadflags=link_flag))
        os.chmod(_BUILD_NEURODAMUS_FNAME, 0o770)

    def install(self, spec, prefix):
        """Install phase.

        bin/ <- special and special-core
        lib/ <- hoc, mod and lib*mech*.so
        share/ <- neuron & coreneuron mod.c's (modc and modc_core)
        python/ If neurodamus-core comes with python, create links
        """
        # base dest dirs already created by model install
        # We install binaries normally, except lib has a suffix
        self._install_binaries(lib_suffix=_LIB_SUFFIX)

        if spec.satisfies('+coreneuron'):
            install = which('nrnivmech_install.sh', path=".")
            install(prefix)

        # Install mods/hocs, and a builder script
        self._install_src(prefix)
        shutil.move(_BUILD_NEURODAMUS_FNAME, prefix.bin)

        # Create mods links in share
        force_symlink(spec['neurodamus-core'].prefix.mod, prefix.share.mod_neurodamus)
        force_symlink(prefix.lib.mod, prefix.share.mod_full)

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

        if self.spec.satisfies("+python"):
            pylib = self.prefix.lib.python
            for m in spack_env.env_modifications:
                if m.name == 'PYTHONPATH':
                    run_env.prepend_path('PYTHONPATH', m.value)
            run_env.prepend_path('PYTHONPATH', pylib)
            run_env.set('NEURODAMUS_PYTHON', pylib)


_BUILD_NEURODAMUS_TPL = """#!/bin/sh
set -e
if [ "$#" -eq 0 ]; then
    echo "******* Neurodamus builder *******"
    echo "Syntax:"
    echo "$(basename $0) <mods_dir> [add_include_flags] [add_link_flags]"
    echo
    echo "NOTE: mods_dir is literally passed to nrnivmodl. If you only have the mechanism mods"
    echo " and wish to build neurodamus you need to include the neurodamus-specific mods."
    echo " Under \\$NEURODAMUS_ROOT/share you'll find the whole set of original mod files, as"
    echo " well as the neurodamus-specific mods alone. You may copy/link them into your directory."
    exit 1
fi

# run with nrnivmodl in path
set -x
'{nrnivmodl}' -incflags '{incflags} '"$2" -loadflags '{loadflags} '"$3" "$1"
"""
