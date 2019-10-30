# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install timemory
#
# You can edit this file again by typing:
#
#     spack edit timemory
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *
import os


class Timemory(CMakePackage):
    """Timing + Memory + Hardware Counter Utilities for C / C++ / CUDA / Python"""

    homepage = "https://timemory.readthedocs.io/en/latest/"
    git = "https://github.com/NERSC/timemory.git"

    version('master', branch='master', submodules=True)

    variant('python', default=True, description="Enable Python support")
    variant('mpi', default=False, description="Enable MPI support")
    variant('papi', default=True, description="Enable PAPI support")
    variant('cuda', default=True, description="Enable CUDA support")
    variant('caliper', default=True, description="Enable Caliper support")
    variant('gperftools', default=True, description="Enable gperftools support")
    variant('cupti', default=True, description="Enable CUPTI support")

    extends('python', when="+python")
    depends_on('python@3:', when="+python")
    depends_on('py-pip', when='+python')
    depends_on('mpi', when='+mpi')
    depends_on('papi', when='+papi')
    depends_on('cuda', when='+cuda')
    depends_on('gperftools', when='+gperftools')
    depends_on('caliper', when='+caliper')
    depends_on('gperftools', when='+gperftools')

    parallel = True

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set PYTHONPATH to include the site-packages directory for the
        extension and any other python extensions it depends on."""

        if '+python' in self.spec:
            # If we set PYTHONHOME, we must also ensure that the corresponding
            # python is found in the build environment. This to prevent cases
            # where a system provided python is run against the standard libraries
            # of a Spack built python. See issue #7128
            spack_env.set('PYTHONHOME', self.home)

            path = os.path.dirname(self.command.path)
            if not is_system_path(path):
                spack_env.prepend_path('PATH', path)

            python_paths = []
            for d in dependent_spec.traverse(
                    deptype=('build', 'run', 'test')):
                if d.package.extends(self.spec):
                    python_paths.append(join_path(d.prefix,
                                                  self.site_packages_dir))

            pythonpath = ':'.join(python_paths)
            spack_env.set('PYTHONPATH', pythonpath)

            # For run time environment set only the path for
            # dependent_spec and prepend it to PYTHONPATH
            if dependent_spec.package.extends(self.spec):
                run_env.prepend_path('PYTHONPATH', join_path(
                    dependent_spec.prefix, self.site_packages_dir))

    def cmake_args(self):
        spec = self.spec

        # Use spack install of Caliper instead of internal build
        args = [
            "-DTIMEMORY_BUILD_CALIPER=OFF",
            "-DTIMEMORY_BUILD_TOOLS=ON",
            "-DTIMEMORY_BUILD_EXTRA_OPTIMIZATIONS=ON",
            "-DTIMEMORY_BUILD_GTEST=OFF",
            "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON",
        ]

        print("{}".format(self.spec))

        if '+python' in spec:
            args.append(
                '-DPYTHON_EXECUTABLE={}'.format(os.path.join(spec['python'].prefix, "bin", "python")))
            args.append('-DTIMEMORY_BUILD_PYTHON=ON')
            args.append("-DTIMEMORY_TLS_MODEL='global-dynamic'")
            python("-m", "pip", "install", "matplotlib", "numpy", "pillow")
        else:
            args.append('-DTIMEMORY_BUILD_PYTHON=OFF')

        if '+caliper' in spec:
            args.append('-DTIMEMORY_USE_CALIPER=ON')
        else:
            args.append('-DTIMEMORY_USE_CALIPER=OFF')

        if '+papi' in spec:
            args.append('-DTIMEMORY_USE_PAPI=ON')
            args.append('-DPAPI_ROOT_DIR={}'.format(spec['papi'].prefix))
        else:
            args.append('-DTIMEMORY_USE_PAPI=OFF')

        if '+mpi' in spec:
            args.append('-DMPI_C_COMPILER={}'.format(spec['mpi'].mpicc))
            args.append('-DMPI_CXX_COMPILER={}'.format(spec['mpi'].mpicxx))
        else:
            args.append('-DTIMEMORY_USE_MPI=OFF')

        if '+cupti' in spec:
            args.append('-DTIMEMORY_USE_CUPTI=ON')
        else:
            args.append('-DTIMEMORY_USE_CUPTI=OFF')

        args.append("-DCMAKE_BUILD_TYPE:STRING=Release")

        return args
