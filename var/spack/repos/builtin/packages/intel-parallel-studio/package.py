from spack import *
import os
import re

from spack.pkg.builtin.intel import IntelInstaller, filter_pick, \
    get_all_components


class IntelParallelStudio(IntelInstaller):
    """Intel Parallel Studio.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # TODO: can also try the online installer (will download files on demand)
    version('composer.2016.2', '1133fb831312eb519f7da897fec223fa',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update2.tgz"
        % os.getcwd())
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
        url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())
    version('cluster.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
        url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())
    version('composer.2016.3', '3208eeabee951fc27579177b593cefe9',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update3.tgz"
        % os.getcwd())
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
        url="file://%s/parallel_studio_xe_2016_update3.tgz" % os.getcwd())
    version('cluster.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
        url="file://%s/parallel_studio_xe_2016_update3.tgz" % os.getcwd())

    variant('rpath', default=True, description="Add rpath to .cfg files")
    variant('newdtags', default=False,
            description="Allow use of --enable-new-dtags in MPI wrappers")
    variant('all', default=False,
            description="Install all files with the requested edition")
    variant('mpi', default=True,
            description="Install the Intel MPI library and ITAC tool")
    variant('mkl', default=True, description="Install the Intel MKL library")
    variant('daal',
            default=True, description="Install the Intel DAAL libraries")
    variant('ipp', default=True, description="Install the Intel IPP libraries")
    variant('tools', default=True, description="Install the Intel Advisor, "
            "VTune Amplifier, and Inspector tools")

    variant('shared', default=True, description='Builds shared library')
    variant('ilp64', default=False, description='64 bit integers')
    variant('openmp', default=False, description='OpenMP multithreading layer')

    provides('mpi', when='@cluster:+mpi')
    provides('mkl', when='+mkl')
    provides('daal', when='+daal')
    provides('ipp', when='+ipp')

    # virtual dependency
    provides('blas', when='+mkl')
    provides('lapack', when='+mkl')
    # TODO: MKL also provides implementation of Scalapack.

    @property
    def blas_libs(self):
        shared = True if '+shared' in self.spec else False
        suffix = dso_suffix if '+shared' in self.spec else 'a'
        mkl_integer = ['libmkl_intel_ilp64'] if '+ilp64' in self.spec else ['libmkl_intel_lp64']  # NOQA: ignore=E501
        mkl_threading = ['libmkl_sequential']
        if '+openmp' in self.spec:
            mkl_threading = ['libmkl_intel_thread', 'libiomp5'] if '%intel' in self.spec else ['libmkl_gnu_thread']  # NOQA: ignore=E501
        # TODO: TBB threading: ['libmkl_tbb_thread', 'libtbb', 'libstdc++']
        mkl_libs = find_libraries(
            mkl_integer + ['libmkl_core'] + mkl_threading,
            root=join_path(self.prefix.lib, 'intel64'),
            shared=shared
        )
        system_libs = [
            'libpthread.{0}'.format(suffix),
            'libm.{0}'.format(suffix),
            'libdl.{0}'.format(suffix)
        ]
        return mkl_libs + system_libs

    @property
    def lapack_libs(self):
        return self.blas_libs

    def check_variants(self, spec):
        error_message = '\t{variant} can not be turned off if "+all" is set'

        if self.spec.satisfies('+all'):
            errors = [error_message.format(variant=x)
                      for x in ('mpi', 'mkl', 'daal', 'ipp', 'tools')
                      if ('~' + x) in self.spec]
            if errors:
                errors = ['incompatible variants given'] + errors
                raise InstallError('\n'.join(errors))

    def install(self, spec, prefix):
        self.check_variants(spec)

        base_components = "ALL"  # when in doubt, install everything
        mpi_components = ""
        mkl_components = ""
        daal_components = ""
        ipp_components = ""

        if not spec.satisfies('+all'):
            all_components = get_all_components()
            regex = '(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)'
            base_components = \
                filter_pick(all_components, re.compile(regex).search)
            regex = '(icsxe|imb|mpi|itac|intel-ta|intel-tc|clck)'
            mpi_components = \
                filter_pick(all_components, re.compile(regex).search)
            mkl_components = \
                filter_pick(all_components, re.compile('(mkl)').search)
            daal_components = \
                filter_pick(all_components, re.compile('(daal)').search)
            ipp_components = \
                filter_pick(all_components, re.compile('(ipp)').search)
            regex = '(gdb|vtune|inspector|advisor)'
            tool_components = \
                filter_pick(all_components, re.compile(regex).search)
            components = base_components

        if not spec.satisfies('+all'):
            if spec.satisfies('+mpi'):
                components += mpi_components
            if spec.satisfies('+mkl'):
                components += mkl_components
            if spec.satisfies('+daal'):
                components += daal_components
            if spec.satisfies('+ipp'):
                components += ipp_components
            if spec.satisfies('+tools') and (spec.satisfies('@cluster') or
                                             spec.satisfies('@professional')):
                components += tool_components

        if spec.satisfies('+all'):
            self.intel_components = 'ALL'
        else:
            self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.dirname(
            os.path.realpath(os.path.join(self.prefix.bin, "icc")))
        abslibdir = os.path.dirname(
            os.path.realpath(os.path.join(
                self.prefix.lib, "intel64", "libimf.a")))

        os.symlink(self.global_license_file, os.path.join(absbindir,
                                                          "license.lic"))
        if spec.satisfies('+tools') and (spec.satisfies('@cluster') or
                                         spec.satisfies('@professional')):
            os.mkdir(os.path.join(self.prefix, "inspector_xe/licenses"))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, "inspector_xe/licenses", "license.lic"))
            os.mkdir(os.path.join(self.prefix, "advisor_xe/licenses"))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, "advisor_xe/licenses", "license.lic"))
            os.mkdir(os.path.join(self.prefix, "vtune_amplifier_xe/licenses"))
            os.symlink(self.global_license_file, os.path.join(
                self.prefix, "vtune_amplifier_xe/licenses", "license.lic"))

        if (spec.satisfies('+all') or spec.satisfies('+mpi')) and \
                spec.satisfies('@cluster'):
            for ifile in os.listdir(os.path.join(self.prefix, "itac")):
                if os.path.isdir(os.path.join(self.prefix, "itac", ifile)):
                    os.symlink(self.global_license_file,
                               os.path.join(self.prefix, "itac", ifile,
                                            "license.lic"))
                if os.path.isdir(os.path.join(self.prefix, "itac",
                                              ifile, "intel64")):
                    os.symlink(self.global_license_file,
                               os.path.join(self.prefix, "itac",
                                            ifile, "intel64",
                                            "license.lic"))
            if spec.satisfies('~newdtags'):
                wrappers = ["mpif77", "mpif77", "mpif90", "mpif90",
                            "mpigcc", "mpigcc", "mpigxx", "mpigxx",
                            "mpiicc", "mpiicc", "mpiicpc", "mpiicpc",
                            "mpiifort", "mpiifort"]
                wrapper_paths = []
                for root, dirs, files in os.walk(spec.prefix):
                    for name in files:
                        if name in wrappers:
                            wrapper_paths.append(os.path.join(spec.prefix,
                                                              root, name))
                for wrapper in wrapper_paths:
                    filter_file(r'-Xlinker --enable-new-dtags', r' ',
                                wrapper)

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %
                                           compiler_command)
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' % abslibdir)

        os.symlink(os.path.join(self.prefix.man, "common", "man1"),
                   os.path.join(self.prefix.man, "man1"))

    def setup_environment(self, spack_env, run_env):
        # TODO: Determine variables needed for the professional edition.

        major_ver = self.version[1]

        # Remove paths that were guessed but are incorrect for this package.
        run_env.remove_path('LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('LD_LIBRARY_PATH',
                            join_path(self.prefix, 'lib'))
        run_env.remove_path('CPATH',
                            join_path(self.prefix, 'include'))

        # Add the default set of variables
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'intel64'))
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib',
                                       'intel64', 'gcc4.4'))
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'tbb', 'include'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'lib', 'mic'))
        run_env.prepend_path('MIC_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))
        run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                             join_path(self.prefix, 'tbb', 'lib', 'mic'))

        if self.spec.satisfies('+all'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix,
                                           'debugger_{0}'.format(major_ver),
                                           'libipt', 'intel64', 'lib'))
            run_env.set('GDBSERVER_MIC',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'gdb',
                                  'targets', 'mic', 'bin', 'gdbserver'))
            run_env.set('GDB_CROSS',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver),
                                  'gdb', 'intel64_mic', 'bin', 'gdb-mic'))
            run_env.set('MPM_LAUNCHER',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'mpm',
                                  'mic',
                                  'bin', 'start_mpm.sh'))
            run_env.set('INTEL_PYTHONHOME',
                        join_path(self.prefix,
                                  'debugger_{0}'.format(major_ver), 'python',
                                  'intel64'))

        if (self.spec.satisfies('+all') or self.spec.satisfies('+mpi')):
            # Only I_MPI_ROOT is set here because setting the various PATH
            # variables will potentially be in conflict with other MPI
            # environment modules. The I_MPI_ROOT environment variable can be
            # used as a base to set necessary PATH variables for using Intel
            # MPI. It is also possible to set the variables in the modules.yaml
            # file if Intel MPI is the dominant, or only, MPI on a system.
            run_env.set('I_MPI_ROOT', join_path(self.prefix, 'impi'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+mkl'):
            spack_env.set('MKLROOT', self.prefix)

            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib',
                                           'intel64'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib',
                                           'intel64'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'mkl', 'include'))
            run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'mkl', 'lib', 'mic'))
            run_env.set('MKLROOT', join_path(self.prefix, 'mkl'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+daal'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'intel64_lin'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'intel64_lin'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'daal', 'include'))
            run_env.prepend_path('CLASSPATH',
                                 join_path(self.prefix, 'daal', 'lib',
                                           'daal.jar'))
            run_env.set('DAALROOT', join_path(self.prefix, 'daal'))

        if self.spec.satisfies('+all') or self.spec.satisfies('+ipp'):
            run_env.prepend_path('LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib',
                                           'intel64'))
            run_env.prepend_path('LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib',
                                           'intel64'))
            run_env.prepend_path('CPATH',
                                 join_path(self.prefix, 'ipp', 'include'))
            run_env.prepend_path('MIC_LD_LIBRARY_PATH',
                                 join_path(self.prefix, 'ipp', 'lib', 'mic'))
            run_env.set('IPPROOT', join_path(self.prefix, 'ipp'))
