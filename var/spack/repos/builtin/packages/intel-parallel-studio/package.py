from spack import *
import os
import re

from spack.pkg.builtin.intel import IntelInstaller, filter_pick, \
    get_all_components


class IntelParallelStudio(IntelInstaller):
    """Intel Parallel Studio.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # TODO: can also try the online installer (will download files on demand)
    version('composer.2016.2', '1133fb831312eb519f7da897fec223fa',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update2.tgz"  # NOQA: ignore=E501
        % os.getcwd())
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
        url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())  # NOQA: ignore=E501
    version('cluster.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
        url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())  # NOQA: ignore=E501
    version('composer.2016.3', '3208eeabee951fc27579177b593cefe9',
        url="file://%s/parallel_studio_xe_2016_composer_edition_update3.tgz"  # NOQA: ignore=E501
        % os.getcwd())
    version('professional.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
        url="file://%s/parallel_studio_xe_2016_update3.tgz" % os.getcwd())  # NOQA: ignore=E501
    version('cluster.2016.3', 'eda19bb0d0d19709197ede58f13443f3',
        url="file://%s/parallel_studio_xe_2016_update3.tgz" % os.getcwd())  # NOQA: ignore=E501

    variant('rpath', default=True, description="Add rpath to .cfg files")
    variant('all', default=False,
            description="Install all files with the requested edition")
    variant('mpi', default=True,
            description="Install the Intel MPI library and ITAC tool")
    variant('mkl', default=True, description="Install the Intel MKL library")
    variant('daal',
            default=True, description="Install the Intel DAAL libraries")
    variant('ipp', default=True, description="Install the Intel IPP libraries")
    variant('tools', default=True, description="""Install the Intel Advisor,\
VTune Amplifier, and Inspector tools""")

    provides('mpi', when='@cluster:+mpi')
    provides('mkl', when='+mkl')
    provides('daal', when='+daal')
    provides('ipp', when='+ipp')

    def install(self, spec, prefix):

        base_components = "ALL"  # when in doubt, install everything
        mpi_components = ""
        mkl_components = ""
        daal_components = ""
        ipp_components = ""

        if spec.satisfies('+all'):
            base_components = "ALL"
        else:
            all_components = get_all_components()
            regex = '(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)'
            base_components = \
                filter_pick(all_components, re.compile(regex).search)
            regex = '(icsxe|imb|mpi|itac|intel-tc|clck)'
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
            if spec.satisfies('+mpi') and 'cluster' in str(spec.version):
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

        self.intel_components = ';'.join(components)
        IntelInstaller.install(self, spec, prefix)

        absbindir = os.path.dirname(os.path.realpath(os.path.join(
            self.prefix.bin, "icc")))
        abslibdir = os.path.dirname(os.path.realpath(os.path.join
                                    (self.prefix.lib, "intel64", "libimf.a")))

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
                os.symlink(self.global_license_file, os.path.join(
                           self.prefix, "itac_latest", "license.lic"))

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %
                                           compiler_command)
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' % abslibdir)

        os.symlink(os.path.join(self.prefix.man, "common", "man1"),
                   os.path.join(self.prefix.man, "man1"))
