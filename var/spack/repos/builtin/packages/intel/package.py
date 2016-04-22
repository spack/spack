from spack import *
import os, re

class Intel(Package):
    """Intel Compilers.

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-parallel-studio-xe"

    # TODO: can also try the online installer (will download files on demand)
    version('composer.2016.2', '1133fb831312eb519f7da897fec223fa',
            url="file://%s/parallel_studio_xe_2016_composer_edition_update2.tgz" % os.getcwd())
    version('professional.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
            url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())
    version('cluster.2016.2', '70be832f2d34c9bf596a5e99d5f2d832',
            url="file://%s/parallel_studio_xe_2016_update2.tgz" % os.getcwd())

    variant('rpath', default=True, description="Add rpath to .cfg files")
    variant('all', default=False, description="Install all files associated with the requested edition")
    variant('mpi', default=True, description="Install the Intel MPI library and ITAC tool")
    variant('mkl', default=True, description="Install the Intel MKL library")
    variant('daal', default=True, description="Install the Intel DAAL libraries")
    variant('ipp', default=True, description="Install the Intel IPP libraries")
    variant('tools', default=True, description="Install the Intel Advisor, VTune Amplifier, and Inspector tools")

    provides('mpi', when='@cluster:+mpi')
    provides('mkl', when='+mkl')
    provides('daal', when='+daal')
    provides('ipp', when='+ipp')

    def install(self, spec, prefix):

        # remove the installation DB, otherwise it will try to install into location of other Intel builds
        try:
            os.remove(os.path.join(os.environ["HOME"], "intel", "intel_sdp_products.db"))
        except OSError:
            pass # if the file does not exist

        # TODO: Update to use pull request 558
        license_path = "/usr/local/etc/license.client.intel.lic"

        base_components = "ALL" # when in doubt, install everything
        mpi_components = ""
        mkl_components = ""
        daal_components = ""
        ipp_components = ""
        tools_components = ""

        def filter_pick(input_list, regex_filter):
            return [l for l in input_list for m in (regex_filter(l),) if m]
        def unfilter_pick(input_list, regex_filter):
            return [l for l in input_list for m in (regex_filter(l),) if not m]
        if spec.satisfies('+all'):
            base_components = "ALL"
        else:
            with open("pset/mediaconfig.xml", "r") as f:
                lines = f.readlines()
                all_components = []
                for line in lines:
                    if line.find('<Abbr>') != -1:
                        component = line[line.find('<Abbr>') + 6:line.find('</Abbr>')]
                        all_components.append(component)
                base_components = filter_pick(all_components, re.compile('(comp|openmp|intel-tbb|icc|ifort|psxe|icsxe-pset)').search)
                mpi_components = filter_pick(all_components, re.compile('(icsxe|imb|mpi|itac|intel-tc|clck)').search)
                mkl_components = filter_pick(all_components, re.compile('(mkl)').search)
                daal_components = filter_pick(all_components, re.compile('(daal)').search)
                ipp_components = filter_pick(all_components, re.compile('(ipp)').search)
                tool_components = filter_pick(all_components, re.compile('(gdb|vtune|inspector|advisor)').search)

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
            if spec.satisfies('+tools') and (spec.satisfies('@cluster') or spec.satisfies('@professional')):
                components += tool_components

        components_string = ''
        for component in components:
            components_string += component + ';'

        silent_config_filename = 'silent.cfg'
        with open(silent_config_filename, 'w') as f:
            f.write("""
ACCEPT_EULA=accept
PSET_MODE=install
CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes
PSET_INSTALL_DIR=%s
ACTIVATION_LICENSE_FILE=%s
ACTIVATION_TYPE=license_file
PHONEHOME_SEND_USAGE_DATA=no
COMPONENTS=%s
""" %(prefix, license_path, components_string))

        install_script = which("install.sh")

        install_script('--silent', silent_config_filename)

        absbindir = os.path.split(os.path.realpath(os.path.join(self.prefix.bin, "icc")))[0]
        abslibdir = os.path.split(os.path.realpath(os.path.join(self.prefix.lib, "intel64", "libimf.a")))[0]

        # symlink or copy?
        os.symlink(license_path, os.path.join(absbindir, "license.lic"))
        if spec.satisfies('+tools') and (spec.satisfies('@cluster') or spec.satisfies('@professional')):
            os.mkdir(os.path.join(self.prefix, "inspector_xe/licenses"))
            os.symlink(license_path, os.path.join(self.prefix, "inspector_xe/licenses", "license.lic"))
            os.mkdir(os.path.join(self.prefix, "advisor_xe/licenses"))
            os.symlink(license_path, os.path.join(self.prefix, "advisor_xe/licenses", "license.lic"))
            os.mkdir(os.path.join(self.prefix, "vtune_amplifier_xe/licenses"))
            os.symlink(license_path, os.path.join(self.prefix, "vtune_amplifier_xe/licenses", "license.lic"))

        if (spec.satisfies('+all') or spec.satisfies('+mpi')) and spec.satisfies('@cluster'):
            os.symlink(license_path, os.path.join(self.prefix, "itac_latest", "license.lic"))

        if spec.satisfies('+rpath'):
            for compiler_command in ["icc", "icpc", "ifort"]:
                cfgfilename = os.path.join(absbindir, "%s.cfg" %(compiler_command))
                with open(cfgfilename, "w") as f:
                    f.write('-Xlinker -rpath -Xlinker %s\n' %(abslibdir))

        os.symlink(os.path.join(self.prefix.man, "common", "man1"), os.path.join(self.prefix.man, "man1"))
