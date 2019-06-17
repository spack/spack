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
    version('2.3.4', git=git, tag='2.3.4', clean=False)
    version('2.3.3', git=git, tag='2.3.3', clean=False)
    version('2.2.1', git=git, tag='2.2.1', clean=False)

    variant('python', default=False, description="Enable Python Neurodamus")
    variant('common', default=False, description="Merge in synapse mechanisms hoc & mods")

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
        if spec.satisfies('+common'):
            copy_all('resources/common/hoc', prefix.hoc)
            copy_all('resources/common/mod', prefix.mod)

        filter_file(r'UNKNOWN_CORE_VERSION', r'%s' % spec.version, prefix.hoc.join('defvar.hoc'))

        try:
            commit_hash = self.fetcher[0].get_commit()
            filter_file(r'UNKNOWN_CORE_HASH', r'\'%s\'' % commit_hash, prefix.hoc.join('defvar.hoc'))
        except Exception as e:
            tty.warn(e)

    def setup_environment(self, spack_env, run_env):
        run_env.set('HOC_LIBRARY_PATH', self.prefix.hoc)
