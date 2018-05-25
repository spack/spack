##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import os
import xml.etree.ElementTree as ET

from llnl.util.filesystem import install
from spack.package import PackageBase, run_after
from spack.util.executable import Executable


def _valid_components():
    """A generator that yields valid components."""

    tree = ET.parse('pset/mediaconfig.xml')
    root = tree.getroot()

    components = root.findall('.//Abbr')
    for component in components:
        yield component.text


class IntelPackage(PackageBase):
    """Specialized class for licensed Intel software.

    This class provides two phases that can be overridden:

    1. :py:meth:`~.IntelPackage.configure`
    2. :py:meth:`~.IntelPackage.install`

    They both have sensible defaults and for many packages the
    only thing necessary will be to override ``setup_environment``
    to set the appropriate environment variables.
    """
    #: Phases of an Intel package
    phases = ['configure', 'install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'IntelPackage'

    #: By default, we assume that all Intel software requires a license.
    #: This can be overridden for packages that do not require a license.
    license_required = True

    #: Comment symbol used in the ``license.lic`` file
    license_comment = '#'

    #: Location where Intel searches for a license file
    license_files = ['Licenses/license.lic']

    #: Environment variables that Intel searches for a license file
    license_vars = ['INTEL_LICENSE_FILE']

    #: URL providing information on how to acquire a license key
    license_url = 'https://software.intel.com/en-us/articles/intel-license-manager-faq'

    #: Components of the package to install.
    #: By default, install 'ALL' components.
    components = ['ALL']

    @property
    def _filtered_components(self):
        """Returns a list or set of valid components that match
        the requested components from ``components``."""

        # Don't filter 'ALL'
        if self.components == ['ALL']:
            return self.components

        # mediaconfig.xml is known to contain duplicate components.
        # If more than one copy of the same component is used, you
        # will get an error message about invalid components.
        # Use a set to store components to prevent duplicates.
        matches = set()

        for valid in _valid_components():
            for requested in self.components:
                if valid.startswith(requested):
                    matches.add(valid)

        return matches

    @property
    def global_license_file(self):
        """Returns the path where a global license file should be stored.

        All Intel software shares the same license, so we store it in a
        common 'intel' directory."""
        return os.path.join(self.global_license_dir, 'intel',
                            os.path.basename(self.license_files[0]))

    def configure(self, spec, prefix):
        """Writes the ``silent.cfg`` file used to configure the installation.

        See https://software.intel.com/en-us/articles/configuration-file-format
        """
        # Patterns used to check silent configuration file
        #
        # anythingpat - any string
        # filepat     - the file location pattern (/path/to/license.lic)
        # lspat       - the license server address pattern (0123@hostname)
        # snpat       - the serial number pattern (ABCD-01234567)
        config = {
            # Accept EULA, valid values are: {accept, decline}
            'ACCEPT_EULA': 'accept',

            # Optional error behavior, valid values are: {yes, no}
            'CONTINUE_WITH_OPTIONAL_ERROR': 'yes',

            # Install location, valid values are: {/opt/intel, filepat}
            'PSET_INSTALL_DIR': prefix,

            # Continue with overwrite of existing installation directory,
            # valid values are: {yes, no}
            'CONTINUE_WITH_INSTALLDIR_OVERWRITE': 'yes',

            # List of components to install,
            # valid values are: {ALL, DEFAULTS, anythingpat}
            'COMPONENTS': ';'.join(self._filtered_components),

            # Installation mode, valid values are: {install, repair, uninstall}
            'PSET_MODE': 'install',

            # Directory for non-RPM database, valid values are: {filepat}
            'NONRPM_DB_DIR': prefix,

            # Perform validation of digital signatures of RPM files,
            # valid values are: {yes, no}
            'SIGNING_ENABLED': 'no',

            # Select target architecture of your applications,
            # valid values are: {IA32, INTEL64, ALL}
            'ARCH_SELECTED': 'ALL',
        }

        # Not all Intel software requires a license. Trying to specify
        # one anyway will cause the installation to fail.
        if self.license_required:
            config.update({
                # License file or license server,
                # valid values are: {lspat, filepat}
                'ACTIVATION_LICENSE_FILE': self.global_license_file,

                # Activation type, valid values are: {exist_lic,
                # license_server, license_file, trial_lic, serial_number}
                'ACTIVATION_TYPE': 'license_file',

                # Intel(R) Software Improvement Program opt-in,
                # valid values are: {yes, no}
                'PHONEHOME_SEND_USAGE_DATA': 'no',
            })

        with open('silent.cfg', 'w') as cfg:
            for key in config:
                cfg.write('{0}={1}\n'.format(key, config[key]))

    def install(self, spec, prefix):
        """Runs the ``install.sh`` installation script."""

        install_script = Executable('./install.sh')
        install_script('--silent', 'silent.cfg')

    @run_after('install')
    def save_silent_cfg(self):
        """Copies the silent.cfg configuration file to ``<prefix>/.spack``."""
        install('silent.cfg', os.path.join(self.prefix, '.spack'))

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
