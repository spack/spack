# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.repo
import spack.spec


def test_false_directives_do_not_exist(mock_packages):
    """Ensure directives that evaluate to False at import time are added to
       dicts on packages.
    """
    cls = spack.repo.path.get_pkg_class('when-directives-false')
    assert not cls.dependencies
    assert not cls.resources
    assert not cls.patches


def test_true_directives_exist(mock_packages):
    """Ensure directives that evaluate to True at import time are added to
       dicts on packages.
    """
    cls = spack.repo.path.get_pkg_class('when-directives-true')

    assert cls.dependencies
    assert spack.spec.Spec() in cls.dependencies['extendee']
    assert spack.spec.Spec() in cls.dependencies['b']

    assert cls.resources
    assert spack.spec.Spec() in cls.resources

    assert cls.patches
    assert spack.spec.Spec() in cls.patches


def test_constraints_from_context(mock_packages):
    pkg_cls = spack.repo.path.get_pkg_class('with-constraint-met')

    assert pkg_cls.dependencies
    assert spack.spec.Spec('@1.0') in pkg_cls.dependencies['b']

    assert pkg_cls.conflicts
    assert (spack.spec.Spec('+foo@1.0'), None) in pkg_cls.conflicts['%gcc']


@pytest.mark.regression('26656')
def test_constraints_from_context_are_merged(mock_packages):
    pkg_cls = spack.repo.path.get_pkg_class('with-constraint-met')

    assert pkg_cls.dependencies
    assert spack.spec.Spec('@0.14:15 ^b@3.8:4.0') in pkg_cls.dependencies['c']


@pytest.mark.regression('27754')
def test_extends_spec(config, mock_packages):
    extender = spack.spec.Spec('extends-spec').concretized()
    extendee = spack.spec.Spec('extendee').concretized()

    assert extender.dependencies
    assert extender.package.extends(extendee)
