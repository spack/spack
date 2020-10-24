# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

class IntelOneapi(Package):
    """
    Includes the icx/ifx compiler executables.
    """

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    version('2021.1.9.2205', sha256='8926a3001e61edbb293cb607beb8eb3a3511330a4625c8f3b1b51603426f121a', url='https://registrationcenter-download.intel.com/akdlm/irc_nas/16949/l_HPCKit_b_2021.1.9.2205_offline.sh', expand=False)

    phases = ['install']

    def install(self, prefix):
        bash = Executable('bash')

        # Capture logs written in /tmp
        tmpdir = tempfile.mkdtemp(prefix='spack-intel-')
        bash.add_default_env('TMPDIR', tmpdir)

        # Need to set HOME to avoid using ~/intel
        bash.add_default_env('HOME', prefix)

        bash('./l_HPCKit_b_%s_offline.sh' %
                       spec.versions.lowest(),
                       '-s', '-a', '-s', '--action', 'install',
                       '--eula', 'accept',
                       '--components',
                       ('intel.oneapi.lin.dpcpp-cpp-compiler-pro'
                        ':intel.oneapi.lin.ifort-compiler'),
                        '--install-dir', prefix)

        # preserve config and logs
        dst = os.path.join(self.prefix, '.spack')
        for f in glob.glob('%s/intel*log' % tmpdir):
            install(f, dst)

    # TODO: this package includes icc as well as icx. Question: is icc a link
    # to icx?
    # @property
    # def cc(self):
    #    pass
