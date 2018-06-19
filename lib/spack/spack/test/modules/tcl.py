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

import pytest
import spack.modules.common
import spack.modules.tcl
import spack.spec

mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf arch=x64-linux'

#: Class of the writer tested in this module
writer_cls = spack.modules.tcl.TclModulefileWriter


@pytest.mark.usefixtures('config', 'mock_packages')
class TestTcl(object):

    def test_simple_case(self, modulefile_content, patch_configuration):
        """Tests the generation of a simple TCL module file."""

        patch_configuration('autoload_direct')
        content = modulefile_content(mpich_spec_string)

        assert 'module-whatis "mpich @3.0.4"' in content

    def test_autoload_direct(self, modulefile_content, patch_configuration):
        """Tests the automatic loading of direct dependencies."""

        patch_configuration('autoload_direct')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content('dtbuild1')

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, patch_configuration):
        """Tests the automatic loading of all dependencies."""

        patch_configuration('autoload_all')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'is-loaded' in x]) == 5
        assert len([x for x in content if 'module load ' in x]) == 5

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content('dtbuild1')

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # The configuration file sets the verbose keyword to True
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 2

    def test_prerequisites_direct(
            self, modulefile_content, patch_configuration
    ):
        """Tests asking direct dependencies as prerequisites."""

        patch_configuration('prerequisites_direct')
        content = modulefile_content('mpileaks arch=x86-linux')

        assert len([x for x in content if 'prereq' in x]) == 2

    def test_prerequisites_all(self, modulefile_content, patch_configuration):
        """Tests asking all dependencies as prerequisites."""

        patch_configuration('prerequisites_all')
        content = modulefile_content('mpileaks arch=x86-linux')

        assert len([x for x in content if 'prereq' in x]) == 5

    def test_alter_environment(self, modulefile_content, patch_configuration):
        """Tests modifications to run-time environment."""

        patch_configuration('alter_environment')
        content = modulefile_content('mpileaks platform=test target=x86_64')

        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 1
        assert len([
            x for x in content if 'setenv OMPI_MCA_mpi_leave_pinned "1"' in x
        ]) == 1
        assert len([
            x for x in content if 'setenv OMPI_MCA_MPI_LEAVE_PINNED "1"' in x
        ]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 1
        assert len([x for x in content if 'setenv MPILEAKS_ROOT' in x]) == 1

        content = modulefile_content(
            'libdwarf %clang platform=test target=x86_32'
        )

        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 0
        assert len([x for x in content if 'is-loaded foo/bar' in x]) == 1
        assert len([x for x in content if 'module load foo/bar' in x]) == 1
        assert len([x for x in content if 'setenv LIBDWARF_ROOT' in x]) == 1

    def test_blacklist(self, modulefile_content, patch_configuration):
        """Tests blacklisting the generation of selected modules."""

        patch_configuration('blacklist')
        content = modulefile_content('mpileaks ^zmpi')

        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

        # Returns a StringIO instead of a string as no module file was written
        with pytest.raises(AttributeError):
            modulefile_content('callpath arch=x86-linux')

        content = modulefile_content('zmpi arch=x86-linux')

        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

    def test_naming_scheme(self, factory, patch_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        patch_configuration('conflicts')

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory('mpileaks')
        expected = '${PACKAGE}/${VERSION}-${COMPILERNAME}'

        assert writer.conf.naming_scheme == expected

    def test_invalid_naming_scheme(self, factory, patch_configuration):
        """Tests the evaluation of an invalid naming scheme."""

        patch_configuration('invalid_naming_scheme')

        # Test that having invalid tokens in the naming scheme raises
        # a RuntimeError
        writer, _ = factory('mpileaks')
        with pytest.raises(RuntimeError):
            writer.layout.use_name

    def test_invalid_token_in_env_name(self, factory, patch_configuration):
        """Tests setting environment variables with an invalid name."""

        patch_configuration('invalid_token_in_env_var_name')

        writer, _ = factory('mpileaks')
        with pytest.raises(RuntimeError):
            writer.write()

    def test_conflicts(self, modulefile_content, patch_configuration):
        """Tests adding conflicts to the module."""

        # This configuration has no error, so check the conflicts directives
        # are there
        patch_configuration('conflicts')
        content = modulefile_content('mpileaks')

        assert len([x for x in content if x.startswith('conflict')]) == 2
        assert len([x for x in content if x == 'conflict mpileaks']) == 1
        assert len([x for x in content if x == 'conflict intel/14.0.1']) == 1

        # This configuration is inconsistent, check an error is raised
        patch_configuration('wrong_conflicts')
        with pytest.raises(SystemExit):
            modulefile_content('mpileaks')

    def test_suffixes(self, patch_configuration, factory):
        """Tests adding suffixes to module file name."""
        patch_configuration('suffix')

        writer, spec = factory('mpileaks+debug arch=x86-linux')
        assert 'foo' in writer.layout.use_name

        writer, spec = factory('mpileaks~debug arch=x86-linux')
        assert 'bar' in writer.layout.use_name

    def test_setup_environment(self, modulefile_content, patch_configuration):
        """Tests the internal set-up of run-time environment."""

        patch_configuration('suffix')
        content = modulefile_content('mpileaks')

        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "mpileaks"' in x]
        ) == 1

        spec = spack.spec.Spec('mpileaks')
        spec.concretize()
        content = modulefile_content(str(spec['callpath']))

        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "callpath"' in x]
        ) == 1

    def test_override_template_in_package(
            self, modulefile_content, patch_configuration
    ):
        """Tests overriding a template from and attribute in the package."""

        patch_configuration('autoload_direct')
        content = modulefile_content('override-module-templates')

        assert 'Override successful!' in content

    def test_override_template_in_modules_yaml(
            self, modulefile_content, patch_configuration
    ):
        """Tests overriding a template from `modules.yaml`"""
        patch_configuration('override_template')

        content = modulefile_content('override-module-templates')
        assert 'Override even better!' in content

        content = modulefile_content('mpileaks arch=x86-linux')
        assert 'Override even better!' in content

    def test_extend_context(
            self, modulefile_content, patch_configuration
    ):
        """Tests using a package defined context"""
        patch_configuration('autoload_direct')
        content = modulefile_content('override-context-templates')

        assert 'puts stderr "sentence from package"' in content

        short_description = 'module-whatis "This package updates the context for TCL modulefiles."'  # NOQA: ignore=E501
        assert short_description in content
