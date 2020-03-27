# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os

import pytest

import spack.config
import spack.package
import spack.cmd.install
from spack.main import SpackCommand

install = SpackCommand('install')
spack_test = SpackCommand('test')


@pytest.fixture()
def mock_test_stage(mutable_config, tmpdir):
    # NOTE: This fixture MUST be applied after any fixture that uses
    # the config fixture under the hood
    # No need to unset because we use mutable_config
    tmp_stage = str(tmpdir.join('test_stage'))
    mutable_config.set('config:test_stage', tmp_stage)

    yield tmp_stage


def test_test_package_not_installed(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    output = spack_test('libdwarf')

    assert "No installed packages match spec libdwarf" in output


@pytest.mark.parametrize('arguments,expected', [
    ([], spack.config.get('config:dirty')),  # default from config file
    (['--clean'], False),
    (['--dirty'], True),
])
def test_test_dirty_flag(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.test.setup_parser(parser)
    args = parser.parse_args(arguments)
    assert args.dirty == expected


def test_test_output(install_mockery, mock_archive, mock_fetch,
                     mock_test_stage):
    """Ensure output printed from pkgs is captured by output redirection."""
    install('printing-package')
    spack_test('printing-package')

    contents = os.listdir(mock_test_stage)
    assert len(contents) == 1

    testdir = os.path.join(mock_test_stage, contents[0])
    contents = os.listdir(testdir)
    assert len(contents) == 1

    outfile = os.path.join(testdir, contents[0])
    with open(outfile, 'r') as f:
        output = f.read()
    assert "BEFORE TEST" in output
    assert "true: expect to succeed" in output
    assert "AFTER TEST" in output
    assert "rror" not in output  # no error


def test_test_output_on_error(mock_packages, mock_archive, mock_fetch,
                              install_mockery, capfd, mock_test_stage):
    install('test-error')
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = spack_test('test-error', fail_on_error=False)

    assert "ProcessError: Command exited with status 1" in out


def test_test_output_on_failure(mock_packages, mock_archive, mock_fetch,
                                install_mockery, capfd, mock_test_stage):
    install('test-fail')
    with capfd.disabled():
        out = spack_test('test-fail', fail_on_error=False)

    assert "Expected 'not in the output' in output of `true`" in out


def test_show_log_on_error(mock_packages, mock_archive, mock_fetch,
                           install_mockery, capfd, mock_test_stage):
    """Make sure spack prints location of test log on failure."""
    install('test-error')
    with capfd.disabled():
        out = spack_test('test-error', fail_on_error=False)

    assert 'See test log' in out
    assert mock_test_stage in out


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'install_mockery'
)
@pytest.mark.parametrize('pkg_name,msgs', [
    ('test-error', ['Error: Command exited', 'ProcessError']),
    ('test-fail', ['Error: Expected', 'AssertionError'])
])
def test_junit_output_with_failures(tmpdir, mock_test_stage, pkg_name, msgs):
    install(pkg_name)
    with tmpdir.as_cwd():
        spack_test(
            '--log-format=junit', '--log-file=test.xml',
            pkg_name)

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="1"' in content
    assert 'errors="0"' in content

    # We want to have both stdout and stderr
    assert '<system-out>' in content
    for msg in msgs:
        assert msg in content


def test_cdash_output_test_error(
        tmpdir, mock_fetch, install_mockery, mock_packages, mock_archive,
        mock_test_stage, capfd):
    install('test-error')
    with tmpdir.as_cwd():
        spack_test(
            '--log-format=cdash',
            '--log-file=cdash_reports',
            'test-error')
        report_dir = tmpdir.join('cdash_reports')
        print(tmpdir.listdir())
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join('test-error_Test.xml')
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert 'Error: Command exited with status 1' in content


def test_cdash_upload_clean_test(
        tmpdir, mock_fetch, install_mockery, mock_packages, mock_archive,
        mock_test_stage):
    install('printing-package')
    with tmpdir.as_cwd():
        spack_test(
            '--log-file=cdash_reports',
            '--log-format=cdash',
            'printing-package')
        report_dir = tmpdir.join('cdash_reports')
        assert report_dir in tmpdir.listdir()
        report_file = report_dir.join('printing-package_Test.xml')
        assert report_file in report_dir.listdir()
        content = report_file.open().read()
        assert '</Test>' in content
        assert '<Text>' not in content


def test_test_help_does_not_show_cdash_options(capsys):
    """Make sure `spack test --help` does not describe CDash arguments"""
    with pytest.raises(SystemExit):
        spack_test('--help')
        captured = capsys.readouterr()
        assert 'CDash URL' not in captured.out


def test_test_help_cdash():
    """Make sure `spack test --help-cdash` describes CDash arguments"""
    out = spack_test('--help-cdash')
    assert 'CDash URL' in out
