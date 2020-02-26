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
    version('1.8.68', sha256='b9d432840aab89d4863c935d3dc604816441eba02d731422b92056cee751ca9c')
    version('1.9.12', sha256='7b623ab9168f460a85d952719ca5249248fc95e6f7a02658b0673b2baa0a8fc6')

    variant('neuron', default=True, description="Use BluePyOpt together with NEURON")

    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-efel', type='run')
    depends_on('py-deap', type='run')
    depends_on('py-scoop@0.7:', type='run')
    depends_on('py-ipyparallel', type='run')
    depends_on('py-pickleshare', type='run')
    depends_on('py-future', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('py-pebble@4.3.10:', type='run')
    depends_on('neuron', type='run', when='+neuron')

    def setup_run_environment(self, env):
        env.unset('PMI_RANK')
        env.set('NEURON_INIT_MPI', "0")
        env.prepend_path('PATH', self.spec['py-ipyparallel'].prefix.bin)
