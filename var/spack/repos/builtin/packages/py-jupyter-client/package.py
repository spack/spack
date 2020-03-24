# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterClient(PythonPackage):
    """Jupyter protocol client APIs"""

    homepage = "https://github.com/jupyter/jupyter_client"
    url      = "https://github.com/jupyter/jupyter_client/archive/4.4.0.tar.gz"

    version('5.3.4', sha256='2af6f0e0e4d88009b11103490bea0bfb405c1c470e226c2b7b17c10e5dda9734')
    version('5.2.4', sha256='61ee1e02fd78b025f9720963e1fe96d8d29f44bc250ca7e7a46bc35a174eb7d6')
    version('4.4.0', sha256='2fda7fe1af35f0b4a77c4a2fd4ee38ac3666ed7f4d92a5b6ff8aaf764c38e199')
    version('4.3.0', sha256='90b6ea3ced910ed94c5d558373490a81b33c672d877c1ffdc76b281e3216f1f6')
    version('4.2.2', sha256='bf3e8ea4c44f07dbe2991e41031f6dab242734be424f4d40b72cc58a12c7d2ca')
    version('4.2.1', sha256='547d443fb38ea667b468a6625ac374d476f8ac90fe17c3e35d75cab3cb8d40ba')
    version('4.2.0', sha256='00eab54615fb10f1e508d8e7a952fbeeb2a82cd67b17582bd61be51a08a61d89')
    version('4.1.1', sha256='ca6f3f66d5dc1e9bca81696ae607a93d652210c3ee9385a7c31c067d5ba88e6e')
    version('4.1.0', sha256='ecf76a159381ec9880fd2c31388c6983b1d855f92f0292cf0667a90dd63f51c0')
    version('4.0.0', sha256='33b15abb1307d8d3716b0d3b5d07aa22fdfbbf65a9f1aedf478a274a6adc11c0')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@5:')
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-pyzmq@13:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'), when='@5:')
    depends_on('py-tornado@4.1:', type=('build', 'run'), when='@5:')
    depends_on('py-setuptools', type='build', when='@5:')
