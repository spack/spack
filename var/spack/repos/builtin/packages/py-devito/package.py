# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-devito
#
# You can edit this file again by typing:
#
#     spack edit py-devito
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyDevito(PythonPackage):
    """Devito is a Python package to implement optimized stencil computation (e.g.,
    finite differences, image processing, machine learning) from high-level symbolic
    problem definitions. Devito builds on SymPy and employs automated code generation
    and just-in-time compilation to execute optimized computational kernels on several
    computer platforms, including CPUs, GPUs, and clusters thereof."""

    homepage = "https://www.devitoproject.org/"
    pypi     = "devito/devito-4.6.2.tar.gz"

    # maintainers = ['github_user1', 'github_user2']

    version('4.6.2', sha256='39c2210a192ad69953b4f8d93440ffd72b07d739c4fe2290e2b182adfb7e143f')

    variant('mpi', default=False, description='Enable MPI support')
    variant('matplotlib', default=False, description='Enable matplolib support')
    variant('pandas', default=False, description='Enable pandas support')

    # FIXME: Only add the python/pip/wheel dependencies if you need specific versions
    # or need to change the dependency type. Generic python/pip/wheel dependencies are
    # added implicity by the PythonPackage base class.
    depends_on('python', type=('build', 'run'))
    depends_on('py-pip@9.0.1:', type='build')
    depends_on('py-versioneer', type='build')
    depends_on('py-setuptools', type='build')
    # depends_on('py-wheel@X.Y:', type='build')

    depends_on('py-numpy@1.16:', type=('build', 'run'))
    depends_on('py-sympy@1.7:1.9', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-flake8@2.1.0:', type=('build', 'run'))
    depends_on('py-nbval', type=('build', 'run'))
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-psutil@5.1.0:5.99', type=('build', 'run'))
    depends_on('py-py-cpuinfo@8:', type=('build', 'run'))
    depends_on('py-cgen@2020.1:', type=('build', 'run'))
    depends_on('py-codepy@2019.1:', type=('build', 'run'))
    depends_on('py-click@:8.99', type=('build', 'run'))
    depends_on('py-codecov', type=('build', 'run'))
    depends_on('py-multidict', type=('build', 'run'))
    depends_on('py-anytree@2.4.3:2.8', type=('build', 'run'))
    depends_on('py-pyrevolve@2.1.3:', type=('build', 'run'))
    depends_on('py-distributed@2022.2:', type=('build', 'run'))
    depends_on('py-pytest@3.6:7.99', type=('build', 'run'))
    depends_on('py-pytest-runner', type=('build', 'run'))
    depends_on('py-pytest-cov', type=('build', 'run'))

    # if MPI
    depends_on('py-mpi4py@:4.0', type=('build', 'run'), when='+mpi')
    depends_on('py-ipyparallel@:8.4', type=('build', 'run'), when='+mpi')

    #if OPTIONAL
    depends_on('py-matplotlib', type=('build', 'run'), when='+matplotlib')
    depends_on('py-pandas', type=('build', 'run'), when='+pandas')


# if NVIDIA

# cupy-cuda110
# dask-cuda
# jupyterlab>=3
# jupyterlab-nvdashboard
# dask_labextension
# fsspec


    # FIXME: Add a build backend, usually defined in pyproject.toml. If no such file
    # exists, use setuptools.
    # depends_on('py-setuptools', type='build')
    # depends_on('py-flit-core', type='build')
    # depends_on('py-poetry-core', type='build')

    # FIXME: Add additional dependencies if required.
    depends_on('mpi', type=('build', 'run'))

    def global_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py
        # FIXME: If not needed, delete this function
        options = []
        return options

    def install_options(self, spec, prefix):
        # FIXME: Add options to pass to setup.py install
        # FIXME: If not needed, delete this function
        options = []
        return options

    @run_before('install')
    def add_examples_dir(self):
        # Add file `__init__py` to examples/ so it is picked up by setuptools
        touch('examples/__init__.py')

    def setup_run_environment(self, env):
        # Make benchmark.py available
        env.prepend_path('DEVITO_HOME', self.prefix)
