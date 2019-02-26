# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class EnvironmentModules(Package):
    """The Environment Modules package provides for the dynamic
    modification of a user's environment via modulefiles."""

    homepage = 'https://modules.readthedocs.io/en/latest/'
    url = 'https://github.com/cea-hpc/modules/archive/v4.2.2.tar.gz'

    version('4.2.2', sha256='7822235e5fdcad85cfa330733672ccf826ee293cec66d34d8c934bc9d454d946')
    version('4.2.1', sha256='4ea403b7bfec0da371dfa7be07d8e68636cef915560fa116196cefd019e5b9e6')
    version('4.2.0', sha256='af2edaaf577fb73af88bd21c10e1f3fd0248434824e6e52febf86ad5d7ba47f8')
    version('4.1.4', sha256='b6902b13660e4c1a7427d7b288a15b65f71e5e5963db6727ce99f3581869abf3')
    version('4.1.3', sha256='6c7f4f11a4a0a64ef20ec3f5ef1c2bb18ac596a7a0e9c79c8377242e65144f5a')
    version('4.1.2', sha256='9fdcd73583e666e2de50a6c43181bb0dae90fdf7dc12924c6f0dc93c316144cc')
    version('4.1.1', sha256='56e7251d883ec6bb5eecd5f0a7d5998936d4137d3587f8580b773f16661aa4fa')
    version('4.1.0', sha256='c909ffc2e3562bc522c9224b71f3e8441b44313aa897915103ec60c44c8c7528')
    version('4.0.0', sha256='8c5b7c0009dea31e99750a4f1ea2083eaf48f68bf0abfa8545c7c3576efa6514')
    version(
        '3.2.10', sha256='fb05c82a83477805a1d97737a9f0ca0db23f69b7bce504f1609ba99477b03955',
        url='http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz'
    )

    variant('X', default=True, description='Build with X functionality')

    # Dependencies:
    depends_on('tcl', type=('build', 'link', 'run'))

    def install(self, spec, prefix):
        tcl_spec = spec['tcl']

        # We are looking for tclConfig.sh
        tcl_config_name = 'tclConfig.sh'
        tcl_config_dir_options = [tcl_spec.prefix.lib,
                                  tcl_spec.prefix.lib64]

        tcl_config_found = False
        for tcl_config_dir in tcl_config_dir_options:
            tcl_config_found = os.path.exists(
                join_path(tcl_config_dir, tcl_config_name))
            if tcl_config_found:
                break

        if not tcl_config_found:
            raise InstallError('Failed to locate ' + tcl_config_name)

        # See: https://sourceforge.net/p/modules/bugs/62/
        cpp_flags = ['-DUSE_INTERP_ERRORLINE']

        config_args = [
            "--without-tclx",
            "--with-tclx-ver=0.0",
            "--prefix=" + prefix,
            # It looks for tclConfig.sh
            "--with-tcl=" + tcl_config_dir,
            "--with-tcl-ver=%d.%d" % (
                tcl_spec.version.version[0], tcl_spec.version.version[1]),
            '--disable-debug',
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            '--disable-versioning',
            '--datarootdir=' + prefix.share,
            'CPPFLAGS=' + ' '.join(cpp_flags)
        ]

        if '~X' in spec:
            config_args = ['--without-x'] + config_args

        configure(*config_args)
        make()
        make('install')
