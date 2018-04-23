##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import inspect

from spack.directives import depends_on
from spack.package import PackageBase, run_after

from llnl.util.filesystem import working_dir


class WafPackage(PackageBase):
    """Specialized class for packages that are built using the
    Waf build system. See https://waf.io/book/ for more information.

    This class provides the following phases that can be overridden:

    * configure
    * build
    * install

    These are all standard Waf commands and can be found by running:

    .. code-block:: console

       $ python waf --help

    Each phase provides a function <phase> that runs:

    .. code-block:: console

       $ python waf -j<jobs> <phase>

    where <jobs> is the number of parallel jobs to build with. Each phase
    also has a <phase_args> function that can pass arguments to this call.
    All of these functions are empty except for the ``configure_args``
    function, which passes ``--prefix=/path/to/installation/prefix``.
    """
    # Default phases
    phases = ['configure', 'build', 'install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'WafPackage'

    # Callback names for build-time test
    build_time_test_callbacks = ['test']

    # Callback names for install-time test
    install_time_test_callbacks = ['installtest']

    # Much like AutotoolsPackage does not require automake and autoconf
    # to build, WafPackage does not require waf to build. It only requires
    # python to run the waf build script.
    depends_on('python@2.5:', type='build')

    @property
    def build_directory(self):
        """The directory containing the ``waf`` file."""
        return self.stage.source_path

    def python(self, *args, **kwargs):
        """The python ``Executable``."""
        inspect.getmodule(self).python(*args, **kwargs)

    def waf(self, *args, **kwargs):
        """Runs the waf ``Executable``."""
        jobs = inspect.getmodule(self).make_jobs

        with working_dir(self.build_directory):
            self.python('waf', '-j{0}'.format(jobs), *args, **kwargs)

    def configure(self, spec, prefix):
        """Configures the project."""
        args = self.configure_args()

        self.waf('configure', *args)

    def configure_args(self):
        """Arguments to pass to configure."""
        return ['--prefix={0}'.format(self.prefix)]

    def build(self, spec, prefix):
        """Executes the build."""
        args = self.build_args()

        self.waf('build', *args)

    def build_args(self):
        """Arguments to pass to build."""
        return []

    def install(self, spec, prefix):
        """Installs the targets on the system."""
        args = self.install_args()

        self.waf('install', *args)

    def install_args(self):
        """Arguments to pass to install."""
        return []

    # Testing

    def test(self):
        """Run unit tests after build.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def installtest(self):
        """Run unit tests after install.

        By default, does nothing. Override this if you want to
        add package-specific tests.
        """
        pass

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
