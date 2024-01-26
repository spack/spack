# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import sys
import tempfile
from contextlib import contextmanager
from io import BytesIO

import pytest

import spack
from spack.main import SpackCommand

logs = SpackCommand("logs")


@contextmanager
def stdout_as_binary_stream():
    original_stdout = sys.stdout

    with tempfile.TemporaryFile(mode="w+b") as tf:
        sys.stdout = tf
        try:
            yield tf
        finally:
            sys.stdout = original_stdout


def _rewind_collect_and_decode(binary_rw_stream):
    binary_rw_stream.seek(0)
    return binary_rw_stream.read().decode("utf-8")


@pytest.fixture
def disable_capture(capfd):
    with capfd.disabled():
        yield


def test_dump_logs(install_mockery, mock_fetch, mock_archive, mock_packages, disable_capture):
    """Test that ``spack log`` can find (and print) the logs for partial
    builds and completed installs.

    Also make sure that for compressed logs, that we automatically
    decompress them.
    """
    cmdline_spec = spack.spec.Spec("libelf")
    concrete_spec = cmdline_spec.concretized()

    # Sanity check, make sure this test is checking what we want: to
    # start with
    assert not concrete_spec.installed

    stage_log_content = """\
test_log stage output
another line
"""
    installed_log_content = """\
test_log install output
here to test multiple lines
"""

    with concrete_spec.package.stage:
        with open(concrete_spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        with stdout_as_binary_stream() as redirected_stdout:
            spack.cmd.logs._logs(cmdline_spec, concrete_spec)
            assert _rewind_collect_and_decode(redirected_stdout) == stage_log_content

    install = SpackCommand("install")
    install("libelf")

    # Sanity check: make sure a path is recorded, regardless of whether
    # it exists (if it does exist, we will overwrite it with content
    # in this test)
    assert concrete_spec.package.install_log_path

    with gzip.open(concrete_spec.package.install_log_path, "wb") as compressed_file:
        bstream = BytesIO(installed_log_content.encode("utf-8"))
        compressed_file.writelines(bstream)

    with stdout_as_binary_stream() as redirected_stdout:
        spack.cmd.logs._logs(cmdline_spec, concrete_spec)
        assert _rewind_collect_and_decode(redirected_stdout) == installed_log_content

    with concrete_spec.package.stage:
        with open(concrete_spec.package.log_path, "w") as f:
            f.write(stage_log_content)
        # We re-create the stage, but "spack log" should ignore that
        # if the package is installed
        with stdout_as_binary_stream() as redirected_stdout:
            spack.cmd.logs._logs(cmdline_spec, concrete_spec)
            assert _rewind_collect_and_decode(redirected_stdout) == installed_log_content
