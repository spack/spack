# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Spack Project Developers. See the top-level COPYRIGHT file for details.
from spack import *
import os
import shutil


class NeurodamusCore(Package):
    """Library of channels developed by Blue Brain Project, EPFL"""

    homepage = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"
    git      = "ssh://bbpcode.epfl.ch/sim/neurodamus-core"

    version('develop', git=git, branch='master')

    variant('python', default=False, description="Enable Python Neurodamus")

    # Neurodamus py is currently an extension to core
    resource(name='pydamus',
             git='ssh://bbpcode.epfl.ch/sim/neurodamus-py',
             when='+python',
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

