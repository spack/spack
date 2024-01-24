# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
from io import BytesIO

import spack
from spack.main import SpackCommand

log = SpackCommand("log")


def test_dump_logs(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that ``spack log`` can find (and print) the logs for partial
    builds and completed installs.

    Also make sure that for compressed logs, that we automatically
    decompress them.
    """
    spec = spack.spec.Spec("libelf").concretized()

    # Sanity check, make sure this test is checking what we want: to
    # start with
    assert not spec.installed

    stage_log_content = """\
test_log stage output
another line
"""
    installed_log_content = """\
test_log install output
here to test multiple lines
"""

    with spec.package.stage:
        with open(spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        assert log("libelf") == stage_log_content

    install = SpackCommand("install")
    install("libelf")

    # Sanity check: make sure a path is recorded, regardless of whether
    # it exists (if it does exist, we will overwrite it with content
    # in this test)
    assert spec.package.install_log_path

    with gzip.open(spec.package.install_log_path, "wb") as compressed_file:
        bstream = BytesIO(installed_log_content.encode("utf-8"))
        compressed_file.writelines(bstream)

    assert log("libelf") == installed_log_content

    with spec.package.stage:
        with open(spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        # We re-create the stage, but "spack log" should ignore that
        # if the package is installed
        assert log("libelf") == installed_log_content
