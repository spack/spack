# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.repo
from spack.spec import Spec


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
    assert Spec() in cls.dependencies['extendee']
    assert Spec() in cls.dependencies['b']

    assert cls.resources
    assert Spec() in cls.resources

    assert cls.patches
    assert Spec() in cls.patches


def test_constraints_from_context(mock_packages):
    pkg_cls = spack.repo.path.get_pkg_class('with-constraint-met')

    assert pkg_cls.dependencies
    assert Spec('@1.0') in pkg_cls.dependencies['b']

    assert pkg_cls.conflicts
    assert (Spec('@1.0'), None) in pkg_cls.conflicts['%gcc']
