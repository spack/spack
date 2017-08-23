##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

import pytest

import spack.cmd.install
from spack.spec import Spec
from spack.main import SpackCommand

install = SpackCommand('install')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    parser = argparse.ArgumentParser()
    spack.cmd.install.setup_parser(parser)
    return parser


@pytest.fixture()
def mock_calls_for_install(monkeypatch):

    class Counter(object):
        def __init__(self):
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1

    monkeypatch.setattr(spack.package.PackageBase, 'do_install', Counter())
    monkeypatch.setattr(spack.package_prefs.PackageTesting, 'test', Counter())
    monkeypatch.setattr(spack.package_prefs.PackageTesting,
                        'test_all', Counter())


def _install_package_and_dependency(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
        install_mockery):

    tmpdir.chdir()
    install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


@pytest.mark.usefixtures('mock_calls_for_install', 'builtin_mock', 'config')
def test_install_runtests():
    install('--test-root', 'dttop')
    assert spack.package_prefs.PackageTesting.test.call_count == 1
    
    install('--test-all', 'a')
    assert spack.package_prefs.PackageTesting.test_all.call_count == 1


def test_install_package_already_installed(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
        install_mockery):

    tmpdir.chdir()
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
    ([], spack.dirty),  # The default read from configuration file
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
