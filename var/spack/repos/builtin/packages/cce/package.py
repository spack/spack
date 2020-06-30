# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re

import llnl.util.tty as tty
import spack.compiler


class Cce(Package):
    """The Cray Compiling Environment"""

    homepage = "https://pubs.cray.com"

    def install(self, spec, prefix):
        raise InstallError(
            'The Cray Compiling Environment is installable, but can be '
            'detected on a system where it is supplied by vendor'
        )

    #: Programming Environment to be loaded on Cray
    cray_prgenv = 'PrgEnv-cray'
    #: Name of the module in Cray's Programming Environment
    cray_module_name = 'cce'
    #: Extra attributes to be used on Cray machines
    cray_extra_attributes = {
        'compilers': {'c': 'cc', 'cxx': 'CC', 'fortran': 'ftn'}
    }

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(r'[Vv]ersion.*?(\d+(\.\d+)+)')
        for version_arg in ('--version', '-V'):
            try:
                output = spack.compiler.get_compiler_version_output(
                    exe, version_arg
                )
                match = version_regex.search(output)
                if match:
                    return match.group(1)
            except spack.util.executable.ProcessError:
                pass
            except Exception as e:
                tty.debug(e)
