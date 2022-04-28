# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import pytest

from spack.directory_layout import DirectoryLayout
from spack.filesystem_view import YamlFilesystemView
from spack.spec import Spec


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_global_activation(install_mockery, mock_fetch):
    """This test ensures that views which are maintained inside of an extendee
       package's prefix are maintained as expected and are compatible with
       global activations prior to #7152.
    """
    spec = Spec('extension1').concretized()
    pkg = spec.package
    pkg.do_install()
    pkg.do_activate()

    extendee_spec = spec['extendee']
    extendee_pkg = spec['extendee'].package
    view = extendee_pkg.view()
    assert pkg.is_activated(view)

    expected_path = os.path.join(
        extendee_spec.prefix, '.spack', 'extensions.yaml')
    assert (view.extensions_layout.extension_file_path(extendee_spec) ==
            expected_path)


@pytest.mark.skipif(sys.platform == 'win32',
                    reason="Not supported on Windows (yet)")
def test_remove_extensions_ordered(install_mockery, mock_fetch, tmpdir):
    view_dir = str(tmpdir.join('view'))
    layout = DirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)
    e2 = Spec('extension2').concretized()
    e2.package.do_install()
    view.add_specs(e2)

    e1 = e2['extension1']
    view.remove_specs(e1, e2)
