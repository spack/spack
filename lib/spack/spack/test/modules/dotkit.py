# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest
import spack.modules.dotkit

#: Class of the writer tested in this module
writer_cls = spack.modules.dotkit.DotkitModulefileWriter


@pytest.mark.usefixtures('config', 'mock_packages')
class TestDotkit(object):

    def test_dotkit(self, modulefile_content, module_configuration):
        """Tests the generation of a dotkit file that loads dependencies
        automatically.
        """

        module_configuration('autoload_direct')
        content = modulefile_content('mpileaks arch=x86-linux')

        assert '#c spack' in content
        assert '#d mpileaks @2.3' in content
        assert len([x for x in content if 'dk_op' in x]) == 2

    def test_override_template_in_package(
            self, modulefile_content, module_configuration
    ):
        """Tests overriding a template from and attribute in the package."""

        module_configuration('autoload_direct')
        content = modulefile_content('override-module-templates')

        assert 'Override successful!' in content

    def test_override_template_in_modules_yaml(
            self, modulefile_content, module_configuration
    ):
        """Tests overriding a template from `modules.yaml`"""

        module_configuration('override_template')

        # Check that this takes precedence over an attribute in the package
        content = modulefile_content('override-module-templates')
        assert 'Override even better!' in content

        content = modulefile_content('mpileaks arch=x86-linux')
        assert 'Override even better!' in content
