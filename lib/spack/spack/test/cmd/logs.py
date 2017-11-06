##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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

import os.path

import pytest

import spack.main
import llnl.util.filesystem as fs
import spack.directory_layout as directory_layout

logs = spack.main.SpackCommand('logs')


@pytest.fixture(scope='function')
def logs_env(tmpdir_factory, monkeypatch, config):
    install_path = tmpdir_factory.mktemp('install_for_database')
    install_layout = directory_layout.YamlDirectoryLayout(str(install_path))

    monkeypatch.setattr(spack.store, 'root', install_path)
    monkeypatch.setattr(spack.store, 'layout', install_layout)

    # Make fake database and fake install directory.
    install_db = spack.database.Database(str(install_path))
    monkeypatch.setattr(spack.store, 'db', install_db)

    pkgs = []

    spec = spack.spec.Spec('libaec@1.0.0')
    spec.concretize()
    pkgs.append(spack.repo.get(spec))

    spec = spack.spec.Spec('libaec@1.0.1')
    spec.concretize()
    pkgs.append(spack.repo.get(spec))

    for pkg in pkgs:
        s = pkg.spec
        pkg.do_install(fake=True)
        dirname = os.path.join(s.prefix, '.spack')
        if '@1.0.1' in s:
            build_out = os.path.join(dirname, 'build.out')
            build_env = os.path.join(dirname, 'build.env')
            fs.touch(build_out)
            fs.touch(build_env)

    yield

    for pkg in pkgs:
        pkg.do_uninstall()


def test_error_cases(logs_env):

    # Error cases are gathered together for performance reasons,
    # as building a mock DB takes some seconds

    out = logs('foo', fail_on_error=False)
    assert logs.returncode == 1
    assert ' matches no installed packages' in out

    out = logs('libaec', fail_on_error=False)
    assert logs.returncode == 1
    assert 'matches multiple packages' in out

    out = logs('libaec@1.0.0', fail_on_error=False)
    assert 'log file does not exist!' in out


def test_logs(logs_env):
    # Just call the command, check it does not fail
    logs('libaec@1.0.1')
