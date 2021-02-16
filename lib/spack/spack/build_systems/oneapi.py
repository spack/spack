# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Common utilities for managing intel oneapi packages.

"""

from os.path import dirname, isdir, join

from spack.package import Package
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable

from llnl.util.filesystem import find_headers, find_libraries


class IntelOneApiPackage(Package):
    """Base class for Intel oneAPI packages."""

    homepage = 'https://software.intel.com/oneapi'

    phases = ['install']

    def component_info(self,
                       dir_name,
                       releases,
                       url_name,
                       components='all'):
        self._dir_name = dir_name
        self._components = components
        self._releases = releases
        self._url_name = url_name

    @staticmethod
    def oneapi_file(package, version, release):
        return 'l_%s_p_%s.%s_offline.sh' % (package, version, release['build'])

    @staticmethod
    def get_url(package, version, release):
        return 'https://registrationcenter-download.intel.com/akdlm/irc_nas/%s/%s' % (
            release['irc_id'],
            IntelOneApiPackage.oneapi_file(package, version, release))

    def url_for_version(self, version):
        return IntelOneApiPackage.get_url(self._url_name,
                                          version,
                                          self._releases[str(version)])

    def install(self, spec, prefix):
        self.install_from_releases(spec, prefix, '.', self._url_name, self._releases)

    def install_from_releases(self, spec, prefix, dir, url_name, releases):
        bash = Executable('bash')

        # Installer writes files in ~/intel set HOME so it goes to prefix
        bash.add_default_env('HOME', prefix)

        version = spec.versions.lowest()
        release = releases[str(version)]
        bash('%s/%s' % (dir,
                        IntelOneApiPackage.oneapi_file(url_name, version, release)),
             '-s', '-a', '-s', '--action', 'install',
             '--eula', 'accept',
             '--components',
             self._components,
             '--install-dir', prefix)
        # Some installers have a bug and do not return an error code when failing
        if not isdir(join(prefix, self._dir_name)):
            raise RuntimeError('install failed')

    def setup_run_environment(self, env):
        self.setup_run_environment_from_dir(env, self._dir_name)

    def setup_run_environment_from_dir(self, env, dir):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/setvars.sh --force
        """
        env.extend(EnvironmentModifications.from_sourcing_file(
            join(self.prefix, dir, 'latest/env/vars.sh')))


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
