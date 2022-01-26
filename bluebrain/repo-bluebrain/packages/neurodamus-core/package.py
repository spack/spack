##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import llnl.util.tty as tty

from spack import *

from .sim_model import SimModel

# Definitions
_CORENRN_MODLIST_FNAME = "coreneuron_modlist.txt"


class NeurodamusCore(SimModel):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "https://bbpgitlab.epfl.ch/hpc/sim/neurodamus-core"
    git      = "git@bbpgitlab.epfl.ch:hpc/sim/neurodamus-core.git"

    version('develop', branch='main', get_full_repo=False)
    version('3.3.3',  tag='3.3.3', get_full_repo=False)
    version('3.3.2',  tag='3.3.2', get_full_repo=False)
    version('3.3.1',  tag='3.3.1', get_full_repo=False)
    version('3.3.0',  tag='3.3.0', get_full_repo=False)
    version('3.2.2',  tag='3.2.2', get_full_repo=False)
    version('3.2.0',  tag='3.2.0', get_full_repo=False)
    version('3.1.0',  tag='3.1.0', get_full_repo=False)
    version('3.0.2',  tag='3.0.2', get_full_repo=False)
    version('3.0.1',  tag='3.0.1', get_full_repo=False)
    version('3.0.0',  tag='3.0.0', get_full_repo=False)
    version('2.11.1', tag='2.11.1', get_full_repo=False)
    version('2.11.0', tag='2.11.0', get_full_repo=False)
    version('2.10.1', tag='2.10.1', get_full_repo=False)
    version('2.10.0', tag='2.10.0', get_full_repo=False)
    version('2.9.3', tag='2.9.3', get_full_repo=False)
    version('2.9.2', tag='2.9.2', get_full_repo=False)
    version('2.9.1', tag='2.9.1', get_full_repo=False)
    version('2.9.0', tag='2.9.0', get_full_repo=False)
    version('2.8.0', tag='2.8.0', get_full_repo=False)
    version('2.7.3', tag='2.7.3', get_full_repo=False)
    version('2.7.2', tag='2.7.2', get_full_repo=False)
    version('2.7.0', tag='2.7.0', get_full_repo=False)
    version('2.6.0', tag='2.6.0', get_full_repo=False)
    version('2.5.0', tag='2.5.0', get_full_repo=False)
    version('2.4.3', tag='2.4.3', get_full_repo=False)
    version('2.4.1', tag='2.4.1', get_full_repo=False)
    version('2.3.4', tag='2.3.4', get_full_repo=False)
    version('2.3.3', tag='2.3.3', get_full_repo=False)
    version('2.2.1', tag='2.2.1', get_full_repo=False)

    variant('mpi',    default=True,  description="Enable MPI support")
    variant('common', default=False, description="Bring in common synapse mechanisms")
    variant('hdf5',   default=True,  description="Enable old Hdf5 reader")
    variant('report', default=True, description="Enable SONATA and binary reporting")
    variant('synapsetool',  default=True, description="Enable SynapseTool reader (for edges)")
    variant('mvdtool',      default=True, description="Enable MVDTool reader (for nodes)")
    # NOTE: Several variants / dependencies come from SimModel

    # Note: We dont request link to MPI so that mpicc can do what is best
    # and dont rpath it so we stay dynamic.
    # 'run' mode will load the same mpi module
    depends_on("mpi",  when='+mpi', type=('build', 'run'))
    depends_on("hdf5+mpi", when='+hdf5+mpi')
    depends_on("hdf5~mpi", when='+hdf5~mpi')
    depends_on('reportinglib',         when='+report')
    depends_on('libsonata-report',     when='+report')
    depends_on('reportinglib+profile', when='+report+profile')
    depends_on('synapsetool',          when='+synapsetool')
    depends_on('py-mvdtool',           when='+mvdtool', type='run')
    # If external & static, we must bring their dependencies.
    depends_on('zlib')  # for hdf5

    resource(name='common',
             git='git@bbpgitlab.epfl.ch:hpc/sim/models/common.git',
             when='+common',
             destination='resources')

    depends_on('python@2.7:', type=('build', 'run'))

    # Dont apply name for now for compat with neuron+binary
    mech_name = ''

    # We want neurodamus-model to fully depend on core, but no modules
    # loaded at runtime. 'link' dependency requires libraries which we
    # dont provide so we override libs to allow an empty LibraryList
    @property
    def libs(self):
        return LibraryList([])

    @run_before('build')
    def prepare(self):
        filter_file(r'UNKNOWN_CORE_VERSION', r'%s' % self.spec.version,
                    join_path('hoc', 'defvar.hoc'))
        try:
            commit_hash = self.fetcher[0].get_commit()
        except Exception as e:
            tty.warn("Error extracting commit hash: " + str(e))
        else:
            filter_file(r'UNKNOWN_CORE_HASH', r"'%s'" % commit_hash[:8],
                        join_path('hoc', 'defvar.hoc'))

        # '+common' will bring common mods.
        # Otherwise build purely neurodamus helper mechs
        if self.spec.satisfies('+common'):
            copy_all('resources/common/hoc', "hoc")
            copy_all('resources/common/mod', "mod")
        else:
            # These two mods are also part of common
            os.remove("mod/VecStim.mod")
            os.remove("mod/netstim_inhpoisson.mod")

        # If we shall build mods for coreneuron,
        # only bring from core those specified
        if self.spec.satisfies("+coreneuron"):
            mkdirp("mod_core")
            with open(join_path("mod", _CORENRN_MODLIST_FNAME)) as core_mods:
                for aux_mod in core_mods:
                    modpath = join_path("mod", aux_mod.strip())
                    if os.path.isfile(modpath):
                        shutil.copy(modpath, 'mod_core')

    def build(self, spec, prefix):
        """ Build mod files from with nrnivmodl / nrnivmodl-core.
            To support shared libs, nrnivmodl is also passed RPATH flags.
        """
        variant_to_compile_flag = {
            "~mpi": "-DDISABLE_MPI",
            "~hdf5": "-DDISABLE_HDF5",
            "~report": "-DDISABLE_REPORTINGLIB",
            "+synapsetool": "-DENABLE_SYNTOOL"
        }

        compile_flags = " ".join(flag for variant,
                                 flag in variant_to_compile_flag.items()
                                 if spec.satisfies(variant))
        self._build_mods('mod', '', compile_flags, 'mod_core')

    # NOTE: install() is inherited

    def setup_run_environment(self, env):
        self._setup_run_environment_common(env)
        for lib in find(self.prefix.lib, 'libnrnmech*'):
            env.set('NRNMECH_LIB_PATH', lib)
