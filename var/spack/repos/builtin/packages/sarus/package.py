# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Sarus(CMakePackage):
    """Sarus is an OCI-compliant container engine for HPC systems."""

    homepage = "https://github.com/eth-cscs/sarus"
    url      = "https://github.com/eth-cscs/sarus/archive/1.3.3.tar.gz"
    git      = "https://github.com/eth-cscs/sarus.git"
    maintainers = ["Madeeks", "teonnik"]

    version('develop', branch='develop')
    version('master',  branch='master')
    version('1.4.0',   tag='1.4.0')
    version('1.3.3',   tag='1.3.3')
    version('1.3.2',   tag='1.3.2')
    version('1.3.1',   tag='1.3.1')
    version('1.3.0',   tag='1.3.0')
    version('1.2.0',   tag='1.2.0')
    version('1.1.0',   tag='1.1.0')
    version('1.0.1',   tag='1.0.1')
    version('1.0.0',   tag='1.0.0')

    variant('ssh', default=True,
            description='Build and install the SSH hook and custom SSH software '
                        'to enable connections inside containers')
    variant('configure_installation', default=True,
            description='Run the script to setup a starting Sarus configuration as '
                        'part of the installation phase. Running the script requires '
                        'super-user privileges.')

    depends_on('wget', type='build')
    depends_on('expat', type='build')
    depends_on('squashfs', type=('build', 'run'))
    depends_on('boost@1.65.0: cxxstd=11')
    depends_on('cpprestsdk@2.10.0:')
    depends_on('libarchive@3.4.1:')
    #depends_on('rapidjson@00dbcf2', type='build')
    depends_on('rapidjson', type='build')
    depends_on('runc')
    depends_on('tini')

    # autoconf is required to build Dropbear for the SSH hook
    depends_on('autoconf', type='build')

    # Python 3 is used to run integration tests
    depends_on('python@3:', type='run', when='@develop')

    def cmake_args(self):
        spec = self.spec
        args = ['-DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_files/gcc.cmake',
                '-DENABLE_SSH=%s' % ('+ssh' in spec)]
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make(*self.install_targets)
            mkdirp(prefix.var.OCIBundleDir)
            #self.install_runc(spec, prefix)
            #self.install_tini(spec, prefix)
            if '+configure_installation' in spec:
                self.configure_installation(spec, prefix)

    #def install_runc(self, spec, prefix):
    #    wget = which('wget')
    #    runc_url = 'https://github.com/opencontainers/runc/releases/download/v1.0.2/runc.amd64'
    #    runc_install_path = prefix.bin + '/runc.amd64'
    #    wget('-O', runc_install_path, runc_url)
    #    set_executable(runc_install_path)

    #def install_tini(self, spec, prefix):
    #    wget = which('wget')
    #    tini_url = 'https://github.com/krallin/tini/releases/download/v0.18.0/tini-static-amd64'
    #    tini_install_path = prefix.bin + '/tini-static-amd64'
    #    wget('-O', tini_install_path, tini_url)
    #    set_executable(tini_install_path)

    def configure_installation(selfself, spec, prefix):
        import subprocess
        script_path = prefix + '/configure_installation.sh'
        subprocess.check_call(script_path)
