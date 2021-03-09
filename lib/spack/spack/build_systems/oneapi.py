# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Common utilities for managing intel oneapi packages.

"""

from os.path import dirname, isdir

from spack.package import Package
from spack.util.executable import Executable

from llnl.util.filesystem import find_headers, find_libraries


class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""

    homepage = 'https://software.intel.com/oneapi'

    phases = ['install']

    def component_info(self,
                       dir_name,
                       components,
                       releases,
                       url_name):
        self._dir_name = dir_name
        self._components = components
        self._releases = releases
        self._url_name = url_name

    def url_for_version(self, version):
        release = self._release(version)
        return 'https://registrationcenter-download.intel.com/akdlm/irc_nas/%s/%s' % (
            release['irc_id'], self._oneapi_file(version, release))

    def install(self, spec, prefix):
        bash = Executable('bash')

        # Installer writes files in ~/intel set HOME so it goes to prefix
        bash.add_default_env('HOME', prefix)

        version = spec.versions.lowest()
        release = self._release(version)
        bash('./%s' % self._oneapi_file(version, release),
             '-s', '-a', '-s', '--action', 'install',
             '--eula', 'accept',
             '--components',
             self._components,
             '--install-dir', prefix)

    #
    # Helper functions
    #

    def _release(self, version):
        return self._releases[str(version)]

    def _oneapi_file(self, version, release):
        return 'l_%s_p_%s.%s_offline.sh' % (
            self._url_name, version, release['build'])


class IntelOneApiLibraryPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI library packages."""

    @property
    def headers(self):
        include_path = '%s/%s/latest/include' % (
            self.prefix, self._dir_name)
        return find_headers('*', include_path, recursive=True)

    @property
    def libs(self):
        lib_path = '%s/%s/latest/lib/intel64' % (self.prefix, self._dir_name)
        lib_path = lib_path if isdir(lib_path) else dirname(lib_path)
        return find_libraries('*', root=lib_path, shared=True, recursive=True)
