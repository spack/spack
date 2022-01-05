##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyBluepyopt(PythonPackage):
    """Bluebrain Python Optimisation Library"""

    homepage = "https://github.com/BlueBrain/BluePyOpt"
    url = "https://pypi.io/packages/source/b/bluepyopt/bluepyopt-1.9.27.tar.gz"

    # NOTE : while adding new release check pmi_rank.patch compatibility
    version('1.10.38', sha256='fb1411c6a8fbfac52d36b837225bae882fd6524acfb4d0580189312ef3c1cfcc')
    version('1.9.37', sha256='4399af71de48b288832e92f0de73c431bf88d6e76e2c4ea250c3b38fb38a45a8')
    version('1.9.27', sha256='4cce15b92b32311c808cae5e005b664deb6e8dc5df4ca13ea7b59252ae346522')
    version('1.8.68', sha256='b9d432840aab89d4863c935d3dc604816441eba02d731422b92056cee751ca9c')
    version('1.6.56', sha256='1c57c91465ca4b947fe157692e7004a3e6df02e4151e3dc77a8831382a8f1ab9')
    version('1.8.68', sha256='b9d432840aab89d4863c935d3dc604816441eba02d731422b92056cee751ca9c')
    version('1.9.12', sha256='7b623ab9168f460a85d952719ca5249248fc95e6f7a02658b0673b2baa0a8fc6')

    # patch required to avoid hpe-mpi linked mechanism library
    patch("pmi_rank.patch", when="@1.9.27:")

    variant('neuron', default=True, description="Use BluePyOpt together with NEURON")

    depends_on('py-setuptools', type='build')
    depends_on('py-pandas', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-efel', type='run')
    depends_on('py-deap', type='run')
    depends_on('py-scoop@0.7:', type='run', when='@:1.9.37')
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
