# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class EnvironmentModules(Package):
    """The Environment Modules package provides for the dynamic
    modification of a user's environment via modulefiles."""

    homepage = "https://sourceforge.net/p/modules/wiki/Home/"
    url = "http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz"

    version('3.2.10', '8b097fdcb90c514d7540bb55a3cb90fb')

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
