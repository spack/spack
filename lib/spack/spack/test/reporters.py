# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import llnl.util.filesystem as fs
import llnl.util.tty as tty

import spack.reporters.extract
import spack.spec
from spack.install_test import TestStatus
from spack.reporters import CDash, CDashConfiguration

# Use a path variable to appease Spack style line length checks
fake_install_prefix = fs.join_path(
    os.sep,
    "usr",
    "spack",
    "spack",
    "opt",
    "spack",
    "linux-rhel7-broadwell",
    "intel-19.0.4.227",
    "fake-1.0",
)
fake_install_test_root = fs.join_path(fake_install_prefix, ".spack", "test")
fake_test_cache = fs.join_path(
    "usr", "spack", ".spack", "test", "abcdefg", "fake-1.0-abcdefg", "cache", "fake"
)


def test_reporters_extract_basics():
    # This test has a description, command, and status
    fake_bin = fs.join_path(fake_install_prefix, "bin", "fake")
    name = "test_no_status"
    desc = "basic description"
    status = TestStatus.PASSED
    outputs = """
==> Testing package fake-1.0-abcdefg
==> [2022-02-15-18:44:21.250165] test: {0}: {1}
==> [2022-02-15-18:44:21.250200] '{2}'
{3}: {0}
""".format(
        name, desc, fake_bin, status
    ).splitlines()

    parts = spack.reporters.extract.extract_test_parts("fake", outputs)
    assert len(parts) == 1
    assert parts[0]["command"] == "{0}".format(fake_bin)
    assert parts[0]["desc"] == desc
    assert parts[0]["loglines"] == ["{0}: {1}".format(status, name)]
    assert parts[0]["status"] == status.lower()


def test_reporters_extract_no_parts(capfd):
    # This test ticks three boxes:
    #  1) has Installing, which is skipped;
    #  2) does not define any test parts;
    #  3) has a status value without a part so generates a warning
    status = TestStatus.NO_TESTS
    outputs = """
==> Testing package fake-1.0-abcdefg
==> [2022-02-11-17:14:38.875259] Installing {0} to {1}
{2}
""".format(
        fake_install_test_root, fake_test_cache, status
    ).splitlines()

    parts = spack.reporters.extract.extract_test_parts("fake", outputs)
    err = capfd.readouterr()[1]

    assert len(parts) == 1
    assert parts[0]["status"] == "notrun"
    assert "No part to add status" in err


def test_reporters_extract_missing_desc():
    # This test includes one part without a description and another with one
    fake_bin = fs.join_path(fake_install_prefix, "bin", "importer")
    names = ["test_fake_bin", "test_fake_util"]
    descs = ["", "import fake util module"]
    failed = TestStatus.FAILED
    passed = TestStatus.PASSED
    results = [passed, failed]
    outputs = """
==> Testing package fake-1.0-abcdefg
==> [2022-02-15-18:44:21.250165] test: {0}:
==> [2022-02-15-18:44:21.250170] '{1}' '-c' 'import fake.bin'
{2}: {0}
==> [2022-02-15-18:44:21.250185] test: {3}: {4}
==> [2022-02-15-18:44:21.250200] '{5}' '-c' 'import fake.util'
{6}: {3}
""".format(
        names[0], descs[0], results[0], names[1], descs[1], fake_bin, results[1]
    ).splitlines()
    for ln in outputs:
        print(ln)

    parts = spack.reporters.extract.extract_test_parts("fake", outputs)

    assert len(parts) == 2
    for i, (name, desc, status) in enumerate(zip(names, descs, results)):
        assert parts[i]["name"] == name
        assert parts[i]["desc"] == desc
        assert parts[i]["status"] == status.lower()


# # TODO/TBD: How will we support this now?
# def test_reporters_extract_xfail():
#     fake_bin = fs.join_path(fake_install_prefix, "bin", "fake-app")
#     outputs = """
# ==> Testing package fake-1.0-abcdefg
# ==> [2022-02-15-18:44:21.250165] Expecting return code in [3]
# ==> [2022-02-15-18:44:21.250165] Expecting return code in [3]
# ==> [2022-02-15-18:44:21.250200] '{0}'
# {1}
# """.format(
#         fake_bin, TestStatus.PASSED
#     ).splitlines()
#
#     parts = spack.reporters.extract.extract_test_parts("fake", outputs)
#
#     assert len(parts) == 1
#     parts[0]["completed"] == "Expected to fail"


@pytest.mark.parametrize("state", [("not installed"), ("external")])
def test_reporters_extract_skipped(state):
    expected = "Skipped {0} package".format(state)
    outputs = """
==> Testing package fake-1.0-abcdefg
{0}
""".format(
        expected
    ).splitlines()

    parts = spack.reporters.extract.extract_test_parts("fake", outputs)

    assert len(parts) == 1
    parts[0]["completed"] == expected


# # TODO/TBD: How will skip tests be handled now?
# def test_reporters_skip():
#     # This test ticks 3 boxes:
#     # 1) covers an as yet uncovered skip messages
#     # 2) covers debug timestamps
#     # 3) unrecognized output
#     fake_bin = fs.join_path(fake_install_prefix, "bin", "fake")
#     unknown_message = "missing timestamp"
#     outputs = """
# ==> Testing package fake-1.0-abcdefg
# ==> [2022-02-15-18:44:21.250165, 123456] Detected the following modules: fake1
# ==> {0}
# ==> [2022-02-15-18:44:21.250175, 123456] running fake program
# ==> [2022-02-15-18:44:21.250200, 123456] '{1}'
# INVALID
# Results for test suite abcdefghijklmn
# """.format(
#         unknown_message, fake_bin
#     ).splitlines()
#
#     parts = spack.reporters.extract.extract_test_parts("fake", outputs)
#
#     assert len(parts) == 1
#     assert fake_bin in parts[0]["command"]
#     assert parts[0]["loglines"] == ["INVALID"]
#     assert parts[0]["elapsed"] == 0.0


def test_reporters_report_for_package_no_stdout(tmpdir, monkeypatch, capfd):
    class MockCDash(CDash):
        def upload(*args, **kwargs):
            # Just return (Do NOT try to upload the report to the fake site)
            return

    configuration = CDashConfiguration(
        upload_url="https://fake-upload",
        packages="fake-package",
        build="fake-cdash-build",
        site="fake-site",
        buildstamp=None,
        track="fake-track",
    )
    monkeypatch.setattr(tty, "_debug", 1)

    reporter = MockCDash(configuration=configuration)
    pkg_data = {"name": "fake-package"}
    reporter.test_report_for_package(tmpdir.strpath, pkg_data, 0)
    err = capfd.readouterr()[1]
    assert "Skipping report for" in err
    assert "No generated output" in err
