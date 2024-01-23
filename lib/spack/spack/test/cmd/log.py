# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import tempfile

import spack
from spack.main import SpackCommand, SpackCommandError

log = SpackCommand("log")


def test_dump_logs(install_mockery, mock_fetch, mock_archive, mock_packages):
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

    with spec.package.stage as stage:
        with open(spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        assert log("libelf") == stage_log_content

    install = SpackCommand("install")
    install("libelf")
    with tempfile.NamedTemporaryFile() as temp_file:
        with open(temp_file.name, "w") as decompressed:
            decompressed.write(installed_log_content)

        with open(temp_file.name, 'rb') as input_file:
            with gzip.open(spec.package.install_log_path, 'wb') as compressed_file:
                compressed_file.writelines(input_file)

    assert log("libelf") == installed_log_content

    with spec.package.stage as stage:
        with open(spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        # We re-create the stage, but "spack log" should ignore that
        # if the package is installed
        assert log("libelf") == installed_log_content