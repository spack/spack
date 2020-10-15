# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package.build_system.cmake import CMakePackage

class CachedCMakePackage(CMakePackage):
    """Specialized class for packages build using CMake initial cache.

    This feature of CMake allows packages to increase reproducibility,
    especially between Spack- and manual builds. It also allows packages to
    sidestep certain parsing bugs in extremely long ``cmake`` commands, and to
    avoid system limits on the length of the command line."""

    phases = ['initconfig', 'cmake', 'build', 'install']

    def cmake_cache_entry(self, name, value, comment=""):
        """Generate a string for a cmake cache variable"""
        return 'set({0} "{1}" CACHE PATH "{2}")\n\n'.format(name, value, comment)


    def cmake_cache_option(self, name, boolean_value, comment=""):
        """Generate a string for a cmake configuration option"""

        value = "ON" if boolean_value else "OFF"
        return 'set({0} {1} CACHE BOOL "{2}")\n\n'.format(name, value, comment)

    @property
    def cache_name(self):
        return "{0}-{1}-{2}-{3}.cmake".format(
            self.name,
            self.spec.architecture,
            self.spec.compiler.name,
            self.spec.compiler.version,
        )

    @property
    def cache_path(self):
        return os.path.join(self.stage.source_path, self.cache_name)

    def flag_handler(self, name, values):
        if name in ('cflags', 'cxxflags', 'cppflags', 'fflags'):
            return (None, None, None)  # handled in the cmake cache
        return (flags, None, None)

    def initconfig_compiler_entries(self):
        entries = [
            "#------------------{0}\n".format("-" * 60),
            "# Compilers\n",
            "#------------------{0}\n\n".format("-" * 60),

            "# Compiler Spec: {0}\n".format(spec.compiler),
            "#------------------{0}\n".format("-" * 60),

            cmake_cache_entry("CMAKE_C_COMPILER", spack_cc),
            cmake_cache_entry("CMAKE_CXX_COMPILER", spack_cxx),
            cmake_cache_entry("CMAKE_Fortran_COMPILER", f_compiler),
        ]

        # use global spack compiler flags
        cppflags = ' '.join(spec.compiler_flags['cppflags'])
        if cppflags:
            # avoid always ending up with ' ' with no flags defined
            cppflags += ' '
        cflags = cppflags + ' '.join(spec.compiler_flags['cflags'])
        if cflags:
            entries.append(cmake_cache_entry("CMAKE_C_FLAGS", cflags))
        cxxflags = cppflags + ' '.join(spec.compiler_flags['cxxflags'])
        if cxxflags:
            entries.append(cmake_cache_entry("CMAKE_CXX_FLAGS", cxxflags))
        fflags = ' '.join(spec.compiler_flags['fflags'])
        if fflags:
            entries.append(cmake_cache_entry("CMAKE_Fortran_FLAGS", fflags))

        return entries

    def initconfig_mpi_entries(self):
        if "mpi" in not in spec:
            return []

        entries = [
            "#------------------{0}\n".format("-" * 60),
            "# MPI\n",
            "#------------------{0}\n\n".format("-" * 60),
        ]

        entries.append(cmake_cache_entry("MPI_C_COMPILER",
                                         spec['mpi'].mpicc))
        entries.append(cmake_cache_entry("MPI_CXX_COMPILER",
                                         spec['mpi'].mpicxx))
        entries.append(cmake_cache_entry("MPI_Fortran_COMPILER",
                                         spec['mpi'].mpifc))

        # Check for slurm
        using_slurm = False
        slurm_checks = ['+slurm',
                        'schedulers=slurm',
                        'process_managers=slurm']
        if any(spec['mpi'].satisfies(variant) for variant in slurm_checks):
            using_slurm = True

        # Determine MPIEXEC
        if using_slurm:
            if spec['mpi'].external:
                # Heuristic until we have dependents on externals
                mpiexec = '/usr/bin/srun'
            else:
                mpiexec = os.path.join(spec['slurm'].prefix.bin, 'srun')
        else:
            mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpirun')
            if not os.path.exists(mpiexec):
                mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpiexec')

        if not os.path.exists(mpiexec):
            msg = "Unable to determine MPIEXEC, %s tests may fail" % self.name
            entries.append("# {0}\n\n".format(msg))
            tty.warn(msg)
        else:
            # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
            # vs the older versions which expect MPIEXEC
            if self.spec["cmake"].satisfies('@3.10:'):
                entries.append(cmake_cache_entry("MPIEXEC_EXECUTABLE",
                                                 mpiexec))
            else:
                entries.append(cmake_cache_entry("MPIEXEC", mpiexec))

        # Determine MPIEXEC_NUMPROC_FLAG
        if using_slurm:
            entries.append(cmake_cache_entry("MPIEXEC_NUMPROC_FLAG", "-n"))
        else:
            entries.append(cmake_cache_entry("MPIEXEC_NUMPROC_FLAG", "-np"))

    def initconfig_hardware_entries(self):
        entries = []
        # Override XL compiler family
        familymsg = ("Override to proper compiler family for XL")
        if (spack_fc is not None) and ("xlf" in spack_fc):
            entries.append(cmake_cache_entry(
                "CMAKE_Fortran_COMPILER_ID", "XL",
                familymsg))
        if "xlc" in spack_cc:
            entries.append(cmake_cache_entry(
                "CMAKE_C_COMPILER_ID", "XL",
                familymsg))
        if "xlC" in spack_cxx:
            entries.append(cmake_cache_entry(
                "CMAKE_CXX_COMPILER_ID", "XL",
                familymsg))

        if 'cuda' in spec:
            entries.append("#------------------{0}\n".format("-" * 60))
            entries.append("# Cuda\n")
            entries.append("#------------------{0}\n\n".format("-" * 60))

            cudatoolkitdir = spec['cuda'].prefix
            entries.append(cmake_cache_entry("CUDA_TOOLKIT_ROOT_DIR",
                                             cudatoolkitdir))
            cudacompiler = "${CUDA_TOOLKIT_ROOT_DIR}/bin/nvcc"
            entries.append(cmake_cache_entry("CMAKE_CUDA_COMPILER",
                                             cudacompiler))

            if "+mpi" in spec:
                entries.append(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER",
                                                 "${MPI_CXX_COMPILER}"))
            else:
                entries.append(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER",
                                                 "${CMAKE_CXX_COMPILER}"))

    def std_initconfig_entries(self):
        return [
            "#------------------{0}\n".format("-" * 60),
            "# !!!! This is a generated file, edit at own risk !!!!\n",
            "#------------------{0}\n".format("-" * 60),
            "# CMake executable path: {0}\n".format(cmake_exe),
            "#------------------{0}\n\n".format("-" * 60),
        ]

    def initconfig(self, spec, prefix):
        cache_entries = (self.initconfig_compiler_entries() +
                         self.initconfig_mpi_entries() +
                         self.initconfig_hardware_entries() +
                         self.initconfig_package_entries())

        with open(self.cache_name, 'w') as f:
            for entry in cache_entries:
                f.write('%s\n' % entry)
            f.write('\n')

    @run_after('install')
    def install_cmake_cache(self):
        mkdirp(self.spec.prefix.share.cmake)
        install(self.cache_path, self.spec.prefix.share.cmake)
