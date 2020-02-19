##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBluepyopt(PythonPackage):
    """Bluebrain Python Optimisation Library"""

    homepage = "https://github.com/BlueBrain/BluePyOpt"
    url = "https://pypi.io/packages/source/b/bluepyopt/bluepyopt-1.6.56.tar.gz"

    version('1.6.56', sha256='1c57c91465ca4b947fe157692e7004a3e6df02e4151e3dc77a8831382a8f1ab9')

    variant('neuron', default=True, description="Use BluePyOpt together with NEURON")

    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-efel', type='run')
    depends_on('py-deap', type='run')
    depends_on('py-ipyparallel', type='run')
    depends_on('py-pickleshare', type='run')
    depends_on('py-future', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('neuron', type='run', when='+neuron')

    def setup_environment(self, spack_env, run_env):
        run_env.unset('PMI_RANK')
        run_env.set('NEURON_INIT_MPI', "0")
        run_env.prepend_path('PATH', self.spec['py-ipyparallel'].prefix.bin)
