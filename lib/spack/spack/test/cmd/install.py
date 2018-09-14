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
import argparse
import os
import filecmp
from six.moves import builtins

import pytest

import llnl.util.filesystem as fs

import spack.config
import spack.package
import spack.cmd.install
from spack.error import SpackError
from spack.spec import Spec
from spack.main import SpackCommand

from six.moves.urllib.error import HTTPError, URLError

install = SpackCommand('install')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    parser = argparse.ArgumentParser()
    spack.cmd.install.setup_parser(parser)
    return parser


@pytest.fixture()
def noop_install(monkeypatch):
    def noop(*args, **kwargs):
        pass
    monkeypatch.setattr(spack.package.PackageBase, 'do_install', noop)


def test_install_package_and_dependency(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


@pytest.mark.disable_clean_stage_check
def test_install_runtests_notests(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert not pkg.run_tests
    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('-v', 'dttop')


@pytest.mark.disable_clean_stage_check
def test_install_runtests_root(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests == (pkg.name == 'dttop')

    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('--test=root', 'dttop')


@pytest.mark.disable_clean_stage_check
def test_install_runtests_all(monkeypatch, mock_packages, install_mockery):
    def check(pkg):
        assert pkg.run_tests

    monkeypatch.setattr(spack.package.PackageBase, 'unit_test_check', check)
    install('--test=all', 'a')
    install('--run-tests', 'a')


def test_install_package_already_installed(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):

    with tmpdir.as_cwd():
        install('libdwarf')
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content

    skipped = [line for line in content.split('\n') if 'skipped' in line]
    assert len(skipped) == 2


@pytest.mark.parametrize('arguments,expected', [
    ([], spack.config.get('config:dirty')),  # default from config file
    (['--clean'], False),
    (['--dirty'], True),
])
def test_install_dirty_flag(parser, arguments, expected):
    args = parser.parse_args(arguments)
    assert args.dirty == expected


def test_package_output(tmpdir, capsys, install_mockery, mock_fetch):
    """Ensure output printed from pkgs is captured by output redirection."""
    # we can't use output capture here because it interferes with Spack's
    # logging. TODO: see whether we can get multiple log_outputs to work
    # when nested AND in pytest
    spec = Spec('printing-package').concretized()
    pkg = spec.package
    pkg.do_install(verbose=True)

    log_file = os.path.join(spec.prefix, '.spack', 'build.out')
    with open(log_file) as f:
        out = f.read()

    # make sure that output from the actual package file appears in the
    # right place in the build log.
    assert "BEFORE INSTALL\n==> './configure'" in out
    assert "'install'\nAFTER INSTALL" in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_build_error(mock_packages, mock_archive, mock_fetch,
                                       config, install_mockery, capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        out = install('build-error', fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.name == 'ProcessError'
    assert 'configure: error: in /path/to/some/file:' in out
    assert 'configure: error: cannot run C compiled programs.' in out


@pytest.mark.disable_clean_stage_check
def test_install_output_on_python_error(
        mock_packages, mock_archive, mock_fetch, config, install_mockery):
    out = install('failing-build', fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.name == 'InstallError'
    assert 'raise InstallError("Expected failure.")' in out


@pytest.mark.disable_clean_stage_check
def test_install_with_source(
        mock_packages, mock_archive, mock_fetch, config, install_mockery):
    """Verify that source has been copied into place."""
    install('--source', '--keep-stage', 'trivial-install-test-package')
    spec = Spec('trivial-install-test-package').concretized()
    src = os.path.join(
        spec.prefix.share, 'trivial-install-test-package', 'src')
    assert filecmp.cmp(os.path.join(mock_archive.path, 'configure'),
                       os.path.join(src, 'configure'))


@pytest.mark.disable_clean_stage_check
def test_show_log_on_error(mock_packages, mock_archive, mock_fetch,
                           config, install_mockery, capfd):
    """Make sure --show-log-on-error works."""
    with capfd.disabled():
        out = install('--show-log-on-error', 'build-error',
                      fail_on_error=False)
    assert isinstance(install.error, spack.build_environment.ChildError)
    assert install.error.pkg.name == 'build-error'
    assert 'Full build log:' in out

    errors = [line for line in out.split('\n')
              if 'configure: error: cannot run C compiled programs' in line]
    assert len(errors) == 2


def test_install_overwrite(
        mock_packages, mock_archive, mock_fetch, config, install_mockery
):
    # It's not possible to overwrite something that is not yet installed
    with pytest.raises(AssertionError):
        install('--overwrite', 'libdwarf')

    # --overwrite requires a single spec
    with pytest.raises(AssertionError):
        install('--overwrite', 'libdwarf', 'libelf')

    # Try to install a spec and then to reinstall it.
    spec = Spec('libdwarf')
    spec.concretize()

    install('libdwarf')

    assert os.path.exists(spec.prefix)
    expected_md5 = fs.hash_directory(spec.prefix)

    # Modify the first installation to be sure the content is not the same
    # as the one after we reinstalled
    with open(os.path.join(spec.prefix, 'only_in_old'), 'w') as f:
        f.write('This content is here to differentiate installations.')

    bad_md5 = fs.hash_directory(spec.prefix)

    assert bad_md5 != expected_md5

    install('--overwrite', '-y', 'libdwarf')
    assert os.path.exists(spec.prefix)
    assert fs.hash_directory(spec.prefix) == expected_md5
    assert fs.hash_directory(spec.prefix) != bad_md5


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery',
)
def test_install_conflicts(conflict_spec):
    # Make sure that spec with conflicts raises a SpackError
    with pytest.raises(SpackError):
        install(conflict_spec)


@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery',
)
def test_install_invalid_spec(invalid_spec):
    # Make sure that invalid specs raise a SpackError
    with pytest.raises(SpackError, match='Unexpected token'):
        install(invalid_spec)


@pytest.mark.usefixtures('noop_install', 'config')
@pytest.mark.parametrize('spec,concretize,error_code', [
    (Spec('mpi'), False, 1),
    (Spec('mpi'), True, 0),
    (Spec('boost'), False, 1),
    (Spec('boost'), True, 0)
])
def test_install_from_file(spec, concretize, error_code, tmpdir):

    if concretize:
        spec.concretize()

    specfile = tmpdir.join('spec.yaml')

    with specfile.open('w') as f:
        spec.to_yaml(f)

    # Relative path to specfile (regression for #6906)
    with fs.working_dir(specfile.dirname):
        # A non-concrete spec will fail to be installed
        install('-f', specfile.basename, fail_on_error=False)
    assert install.returncode == error_code

    # Absolute path to specfile (regression for #6983)
    install('-f', str(specfile), fail_on_error=False)
    assert install.returncode == error_code


@pytest.mark.disable_clean_stage_check
@pytest.mark.usefixtures(
    'mock_packages', 'mock_archive', 'mock_fetch', 'config', 'install_mockery'
)
@pytest.mark.parametrize('exc_typename,msg', [
    ('RuntimeError', 'something weird happened'),
    ('ValueError', 'spec is not concrete')
])
def test_junit_output_with_failures(tmpdir, exc_typename, msg):
    with tmpdir.as_cwd():
        install(
            '--log-format=junit', '--log-file=test.xml',
            'raiser',
            'exc_type={0}'.format(exc_typename),
            'msg="{0}"'.format(msg)
        )

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
    assert msg in content


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize('exc_typename,msg', [
    ('RuntimeError', 'something weird happened'),
    ('KeyboardInterrupt', 'Ctrl-C strikes again')
])
def test_junit_output_with_errors(
        exc_typename, msg,
        mock_packages, mock_archive, mock_fetch, install_mockery,
        config, tmpdir, monkeypatch):

    def just_throw(*args, **kwargs):
        exc_type = getattr(builtins, exc_typename)
        raise exc_type(msg)

    monkeypatch.setattr(spack.package.PackageBase, 'do_install', just_throw)

    with tmpdir.as_cwd():
        install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()

    # Count failures and errors correctly
    assert 'tests="1"' in content
    assert 'failures="0"' in content
    assert 'errors="1"' in content

    # We want to have both stdout and stderr
    assert '<system-out>' in content
    assert msg in content


@pytest.mark.usefixtures('noop_install', 'config')
@pytest.mark.parametrize('clispecs,filespecs', [
    [[],                  ['mpi']],
    [[],                  ['mpi', 'boost']],
    [['cmake'],           ['mpi']],
    [['cmake', 'libelf'], []],
    [['cmake', 'libelf'], ['mpi', 'boost']],
])
def test_install_mix_cli_and_files(clispecs, filespecs, tmpdir):

    args = clispecs

    for spec in filespecs:
        filepath = tmpdir.join(spec + '.yaml')
        args = ['-f', str(filepath)] + args
        s = Spec(spec)
        s.concretize()
        with filepath.open('w') as f:
            s.to_yaml(f)

    install(*args, fail_on_error=False)
    assert install.returncode == 0


def test_extra_files_are_archived(mock_packages, mock_archive, mock_fetch,
                                  config, install_mockery):
    s = Spec('archive-files')
    s.concretize()

    install('archive-files')

    archive_dir = os.path.join(
        spack.store.layout.metadata_path(s), 'archived-files'
    )
    config_log = os.path.join(archive_dir, 'config.log')
    assert os.path.exists(config_log)

    errors_txt = os.path.join(archive_dir, 'errors.txt')
    assert os.path.exists(errors_txt)


@pytest.mark.disable_clean_stage_check
def test_cdash_report_concretization_error(tmpdir, mock_fetch, install_mockery,
                                           capfd, conflict_spec):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises(SpackError):
                install(
                    '--log-format=cdash',
                    '--log-file=cdash_reports',
                    conflict_spec)
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('Update.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert '<UpdateReturnStatus>Conflicts in concretized spec' \
                in content


@pytest.mark.disable_clean_stage_check
def test_cdash_upload_build_error(tmpdir, mock_fetch, install_mockery,
                                  capfd):
    # capfd interferes with Spack's capturing
    with capfd.disabled():
        with tmpdir.as_cwd():
            with pytest.raises((HTTPError, URLError)):
                install(
                    '--log-format=cdash',
                    '--log-file=cdash_reports',
                    '--cdash-upload-url=http://localhost/fakeurl/submit.php?project=Spack',
                    'build-error')
            report_dir = tmpdir.join('cdash_reports')
            assert report_dir in tmpdir.listdir()
            report_file = report_dir.join('Build.xml')
            assert report_file in report_dir.listdir()
            content = report_file.open().read()
            assert '<Text>configure: error: in /path/to/some/file:</Text>' in content


@pytest.mark.disable_clean_stage_check
def test_build_error_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ''
        try:
            install('build-error')
            assert False, "no exception was raised!"
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert 'configure: error: in /path/to/some/file:' in msg
        assert 'configure: error: cannot run C compiled programs.' in msg


@pytest.mark.disable_clean_stage_check
def test_build_warning_output(tmpdir, mock_fetch, install_mockery, capfd):
    with capfd.disabled():
        msg = ''
        try:
            install('build-warnings')
        except spack.build_environment.ChildError as e:
            msg = e.long_message

        assert 'WARNING: ALL CAPITAL WARNING!' in msg
        assert 'foo.c:89: warning: some weird warning!' in msg
