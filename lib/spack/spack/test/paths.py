# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.paths as paths
import os
import pathlib


def test_install_location(working_env, tmpdir):
    base_prefix = str(tmpdir.join("prefix").ensure(dir=True))
    xdg_data_home = str(tmpdir.join("xdg_data_home"))
    os.environ["XDG_DATA_HOME"] = xdg_data_home
    p1 = paths.SpackPaths(base_prefix)
    assert p1.default_install_location == str(pathlib.Path(xdg_data_home) / "spack" / "installs")

    # Check that SPACK_DATA_HOME overrides
    spack_data_home = str(tmpdir.join("spack_data_home"))
    os.environ["SPACK_DATA_HOME"] = spack_data_home
    p2 = paths.SpackPaths(base_prefix)
    assert p2.default_install_location == str(pathlib.Path(spack_data_home) / "installs")