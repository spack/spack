from spack import *
import os

class Intel(Package):
    """Intel Compilers.

    Note: You will have to add add the downolad file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "http://www.intel.com"

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

        if spec.satisfies('+all'):
            base_components = "ALL"
        elif '2016' in str(spec.version): # TODO: string conversion of the spec version is admittedly not the best mechanism 
            base_components = "intel-comp-l-all-vars__noarch;intel-comp-l-all-common__noarch;intel-comp-l-ps-common__noarch;intel-comp-l-all-devel__x86_64;intel-comp-l-ps-devel__x86_64;intel-comp-l-ps-ss-devel__x86_64;intel-openmp-l-all__x86_64;intel-openmp-l-ps-mic__x86_64;intel-openmp-l-ps__x86_64;intel-openmp-l-ps-ss__x86_64;intel-openmp-l-all-devel__x86_64;intel-openmp-l-ps-mic-devel__x86_64;intel-openmp-l-ps-devel__x86_64;intel-openmp-l-ps-devel-jp__x86_64;intel-openmp-l-ps-mic-devel-jp__x86_64;intel-openmp-l-ps-ss-devel__x86_64;intel-tbb-libs__noarch;intel-comp-all-doc__noarch;intel-comp-ps-ss-doc__noarch;intel-comp-ps-doc-jp__noarch;intel-icc-doc__noarch;intel-icc-ps-doc__noarch;intel-icc-ps-doc-jp__noarch;intel-icc-ps-ss-doc__noarch;intel-ifort-ps-doc__noarch;intel-ifort-ps-doc-jp__noarch;intel-icc-l-all__x86_64;intel-icc-l-ps-ss__x86_64;intel-icc-l-all-vars__noarch;intel-icc-l-all-common__noarch;intel-icc-l-ps-common__noarch;intel-icc-l-all-devel__x86_64;intel-icc-l-ps-devel__x86_64;intel-icc-l-ps-ss-devel__x86_64;intel-ifort-l-ps-jp__x86_64;intel-ifort-l-ps__x86_64;intel-ifort-l-ps-vars__noarch;intel-ifort-l-ps-common__noarch;intel-ifort-l-ps-devel__x86_64;intel-tbb-devel__noarch;intel-tbb-common__noarch;intel-tbb-ps-common__noarch;intel-tbb-common-jp__noarch;intel-tbb-doc__noarch;intel-tbb-doc-jp__noarch;intel-psxe-common__noarch;intel-psxe-doc__noarch;intel-ccomp-doc__noarch;intel-fcomp-doc__noarch;intel-compxe-doc__noarch;intel-icsxe-pset"
            mpi_components = "intel-imb__x86_64;intel-mpi-rt-core__x86_64;intel-mpi-rt-mic__x86_64;intel-mpi-sdk-core__x86_64;intel-mpi-sdk-mic__x86_64;intel-mpi-doc__x86_64;intel-itac-common__noarch;intel-ta__x86_64;intel-tc__x86_64;intel-tc-mic__x86_64;intel-itac-common-pset__noarch;intel_clck_common__x86_64;intel_clck_analyzer__x86_64;intel_clck_collector__x86_64;intel_clck_database__x86_64;intel_clck_common-pset__noarch;intel-icsxe__noarch;intel-psf-intel__x86_64;intel-icsxe-doc__noarc"
            mkl_components = "intel-mkl__x86_64;intel-mkl-ps__x86_64;intel-mkl-ps-jp__x86_64;intel-mkl-common__noarch;intel-mkl-ps-common__noarch;intel-mkl-ps-common-jp__noarch;intel-mkl-devel__x86_64;intel-mkl-ps-mic-devel__x86_64;intel-mkl-ps-f95-devel__x86_64;intel-mkl-gnu-devel__x86_64;intel-mkl-ps-gnu-devel__x86_64;intel-mkl-ps-pgi-devel__x86_64;intel-mkl-ps-cluster-devel__x86_64;intel-mkl-ps-cluster-common__noarch;intel-mkl-ps-f95-common__noarch;intel-mkl-ps-cluster__x86_64;intel-mkl-gnu__x86_64;intel-mkl-ps-gnu__x86_64;intel-mkl-ps-pgi__x86_64;intel-mkl-ps-mic__x86_64;intel-mkl-ps-mic-jp__x86_64;intel-mkl-doc__noarch;intel-mkl-ps-doc__noarch;intel-mkl-ps-doc-jp__noarch;intel-mkl-ps-ss-tbb__x86_64;intel-mkl-ps-ss-tbb-devel__x86_64;intel-mkl-ps-tbb-mic__x86_64;intel-mkl-ps-tbb-mic-devel__x86_64"
            daal_components = "intel-daal__x86_64;intel-daal-common__noarch;intel-daal-ps-common-jp__noarch;intel-daal-doc__noarch;intel-daal-ps-doc-jp__noarch"
            ipp_components = "intel-ipp-l-common__noarch;intel-ipp-l-ps-common__noarch;intel-ipp-l-st__x86_64;intel-ipp-l-mt__x86_64;intel-ipp-l-st-devel__x86_64;intel-ipp-l-ps-st-devel__x86_64;intel-ipp-l-mt-devel__x86_64;intel-ipp-l-doc__noarch;intel-ipp-l-ps-doc-jp__noarch"
            tools_components = "intel-gdb-gt__x86_64;intel-gdb-gt-libelfdwarf__x86_64;intel-gdb-gt-devel__x86_64;intel-gdb-gt-common__noarch;intel-gdb-gt-doc__noarch;intel-gdb-ps-cdt__x86_64;intel-gdb-ps-cdt-source__x86_64;intel-gdb-ps-mic__x86_64;intel-gdb-ps-mpm__x86_64;intel-gdb-ps-doc__noarch;intel-gdb-ps-doc-jp__noarch;intel-gdb__x86_64;intel-gdb-common__noarch;intel-gdb-doc__noarch;intel-gdb-doc-jp__noarch;intel-gdb-gt-src__noarch;intel-gdb-source__noarch;intel-compxe__noarch;intel-gdb-ps-common__noarch;intel-vtune-amplifier-xe-2016-cli__i486;intel-vtune-amplifier-xe-2016-cli__x86_64;intel-vtune-amplifier-xe-2016-common__noarch;intel-vtune-amplifier-xe-2016-cli-common__noarch;intel-vtune-amplifier-xe-2016-collector-32linux__i486;intel-vtune-amplifier-xe-2016-collector-64linux__x86_64;intel-vtune-amplifier-xe-2016-doc__noarch;intel-vtune-amplifier-xe-2016-sep__noarch;intel-vtune-amplifier-xe-2016-gui-common__noarch;intel-vtune-amplifier-xe-2016-gui__x86_64;intel-vtune-amplifier-xe-2016-common-pset__noarch;intel-inspector-xe-2016-cli__i486;intel-inspector-xe-2016-cli__x86_64;intel-inspector-xe-2016-cli-common__noarch;intel-inspector-xe-2016-doc__noarch;intel-inspector-xe-2016-gui-common__noarch;intel-inspector-xe-2016-gui__x86_64;intel-inspector-xe-2016-cli-pset__noarch;intel-advisor-xe-2016-cli__i486;intel-advisor-xe-2016-cli__x86_64;intel-advisor-xe-2016-cli-common__noarch;intel-advisor-xe-2016-doc__noarch;intel-advisor-xe-2016-gui-common__noarch;intel-advisor-xe-2016-gui__i486;intel-advisor-xe-2016-gui__x86_64;intel-advisor-xe-2016-cli-pset__noarch"

        components = base_components
        if not spec.satisfies('+all'):
            if spec.satisfies('+mpi') and 'cluster' in str(spec.version):
                components += ";" + mpi_components
            if spec.satisfies('+mkl'):
                components += ";" + mkl_components
            if spec.satisfies('+daal'):
                components += ";" + daal_components
            if spec.satisfies('+ipp'):
                components += ";" + ipp_components
            if spec.satisfies('+tools') and (spec.satisfies('@cluster') or spec.satisfies('@professional')):
                components += ";" + tools_components

        with open('install.ini', 'w') as f:
            f.write("""
ACCEPT_EULA=accept
PSET_MODE=install
CONTINUE_WITH_INSTALLDIR_OVERWRITE=yes
PSET_INSTALL_DIR=%s
ACTIVATION_LICENSE_FILE=%s
ACTIVATION_TYPE=license_file
PHONEHOME_SEND_USAGE_DATA=no
COMPONENTS=%s
""" %(prefix, license_path, components))

        install_script = which("install.sh")

        install_script('--silent', 'install.ini')

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
