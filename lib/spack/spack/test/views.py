# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

from spack.directory_layout import DirectoryLayout
from spack.filesystem_view import YamlFilesystemView
from spack.spec import Spec


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_remove_extensions_ordered(install_mockery, mock_fetch, tmpdir):
    view_dir = str(tmpdir.join("view"))
    layout = DirectoryLayout(view_dir)
    view = YamlFilesystemView(view_dir, layout)
    e2 = Spec("extension2").concretized()
    e2.package.do_install()
    view.add_specs(e2)

    e1 = e2["extension1"]
    view.remove_specs(e1, e2)
