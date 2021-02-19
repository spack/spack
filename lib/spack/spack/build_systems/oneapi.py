# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Common utilities for managing intel oneapi packages.

"""

import glob
from os.path import dirname, isdir, join
import subprocess

from spack.directives import depends_on
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

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/setvars.sh --force
        """
        env.extend(EnvironmentModifications.from_sourcing_file(
            join(self.prefix, 'setvars.sh'), '--force'))

    # Helper functions
    #

    def _release(self, version):
        return self._releases[str(version)]

    def _oneapi_file(self, version, release):
        return 'l_%s_p_%s.%s_offline.sh' % (
            self._url_name, version, release['build'])


class IntelOneApiCompilerPackage(IntelOneApiPackage):
    """Base class for Intel oneAPI compiler packages."""

    depends_on('patchelf', type='build')

    def _join_prefix(self, path):
        return join(self.prefix, 'compiler/latest/linux', path)

    def _ld_library_path(self):
        dirs = ['lib',
                'lib/x64',
                'lib/emu',
                'lib/oclfpga/host/linux64/lib',
                'lib/oclfpga/linux64/lib',
                'compiler/lib/intel64_lin',
                'compiler/lib']
        for dir in dirs:
            yield self._join_prefix(dir)

    def install(self, spec, prefix):
        super(IntelOneApiCompilerPackage, self).install(spec, prefix)

        rpath = ':'.join(self._ld_library_path())
        patch_dirs = ['compiler/lib/intel64_lin',
                      'compiler/lib/intel64',
                      'bin']
        for pd in patch_dirs:
            for file in glob.glob(self._join_prefix(join(pd, '*'))):
                # Try to patch all files, patchelf will do nothing if
                # file should not be patched
                subprocess.call(['patchelf', '--set-rpath', rpath, file])


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
