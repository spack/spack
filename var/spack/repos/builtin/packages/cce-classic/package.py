# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class CceClassic(Package):
    """The Cray Compiling Environment (Classic CRAY frontend)"""

    homepage = "https://pubs.cray.com"

    def install(self, spec, prefix):
        raise InstallError(
            'The Cray Compiling Environment is not installable, but can be '
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
    def cray_spec_version(cls, module_version):
        if module_version.endswith('-classic'):
            return module_version.replace('-classic', '')
        if module_version > '9':
            return None
        return module_version

    cc = 'cc'
    cxx = 'CC'
    fortran = 'ftn'
