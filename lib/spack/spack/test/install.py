##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os
import pytest

import spack
import spack.store
from spack.spec import Spec


def test_install_and_uninstall(install_mockery, mock_fetch):
    # Get a basic concrete spec for the trivial install package.
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete

    # Get the package
    pkg = spack.repo.get(spec)

    try:
        pkg.do_install()
        pkg.do_uninstall()
    except Exception:
        pkg.remove_prefix()
        raise


def mock_remove_prefix(*args):
    raise MockInstallError(
        "Intentional error",
        "Mock remove_prefix method intentionally fails")


class RemovePrefixChecker(object):
    def __init__(self, wrapped_rm_prefix):
        self.removed = False
        self.wrapped_rm_prefix = wrapped_rm_prefix

    def remove_prefix(self):
        self.removed = True
        self.wrapped_rm_prefix()


class MockStage(object):
    def __init__(self, wrapped_stage):
        self.wrapped_stage = wrapped_stage
        self.test_destroyed = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return True

    def destroy(self):
        self.test_destroyed = True
        self.wrapped_stage.destroy()

    def __getattr__(self, attr):
        return getattr(self.wrapped_stage, attr)


def test_partial_install_delete_prefix_and_stage(install_mockery, mock_fetch):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    remove_prefix = spack.package.Package.remove_prefix
    instance_rm_prefix = pkg.remove_prefix

    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        with pytest.raises(MockInstallError):
            pkg.do_install()
        assert os.path.isdir(pkg.prefix)
        rm_prefix_checker = RemovePrefixChecker(instance_rm_prefix)
        spack.package.Package.remove_prefix = rm_prefix_checker.remove_prefix
        setattr(pkg, 'succeed', True)
        pkg.stage = MockStage(pkg.stage)
        pkg.do_install(restage=True)
        assert rm_prefix_checker.removed
        assert pkg.stage.test_destroyed
        assert pkg.installed
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        pkg._stage = None
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


def test_partial_install_keep_prefix(install_mockery, mock_fetch):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    # Normally the stage should start unset, but other tests set it
    pkg._stage = None
    remove_prefix = spack.package.Package.remove_prefix
    try:
        # If remove_prefix is called at any point in this test, that is an
        # error
        spack.package.Package.remove_prefix = mock_remove_prefix
        with pytest.raises(spack.build_environment.ChildError):
            pkg.do_install(keep_prefix=True)
        assert os.path.exists(pkg.prefix)
        setattr(pkg, 'succeed', True)
        pkg.stage = MockStage(pkg.stage)
        pkg.do_install(keep_prefix=True)
        assert pkg.installed
        assert not pkg.stage.test_destroyed
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        pkg._stage = None
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


def test_second_install_no_overwrite_first(install_mockery, mock_fetch):
    spec = Spec('canfail')
    spec.concretize()
    pkg = spack.repo.get(spec)
    remove_prefix = spack.package.Package.remove_prefix
    try:
        spack.package.Package.remove_prefix = mock_remove_prefix
        setattr(pkg, 'succeed', True)
        pkg.do_install()
        assert pkg.installed
        # If Package.install is called after this point, it will fail
        delattr(pkg, 'succeed')
        pkg.do_install()
    finally:
        spack.package.Package.remove_prefix = remove_prefix
        try:
            delattr(pkg, 'succeed')
        except AttributeError:
            pass


def test_store(install_mockery, mock_fetch):
    spec = Spec('cmake-client').concretized()
    pkg = spec.package
    pkg.do_install()


def test_failing_build(install_mockery, mock_fetch):
    spec = Spec('failing-build').concretized()
    pkg = spec.package
    with pytest.raises(spack.build_environment.ChildError):
        pkg.do_install()


class MockInstallError(spack.error.SpackError):
    pass
