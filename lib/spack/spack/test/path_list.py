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
"""Test lazily computed path attributes on packages."""
import os
import pytest

import spack
from spack.spec import Spec


def test_simple_pathattr(builtin_mock, config):
    spec = Spec('has-path-attr').concretized()
    pkg = spack.repo.get(spec)
    assert pkg.simple_path_list == 'include'
    assert pkg.path_list('simple_path_list') == [
        os.path.join(pkg.prefix, 'include')]


def test_no_such_pathattr(builtin_mock, config):
    spec = Spec('has-path-attr').concretized()
    pkg = spack.repo.get(spec)

    with pytest.raises(AttributeError):
        pkg.path_list('xxxx')


def test_version_pathattr(builtin_mock, config):
    spec3 = Spec('has-path-attr').concretized()
    pkg3 = spack.repo.get(spec3)

    assert pkg3.path_list('short_version_path_list') == [
        os.path.join(pkg3.prefix, 'example/pkg-1.3')]
    assert pkg3.path_list('long_version_path_list')  == [
        os.path.join(pkg3.prefix, 'example/pkg-1.3.0')]

    spec2 = Spec('has-path-attr@1.2.0').concretized()
    pkg2 = spack.repo.get(spec2)

    spec1 = Spec('has-path-attr@1.1.0').concretized()
    pkg1 = spack.repo.get(spec1)

    assert pkg2.path_list('short_version_path_list') == [
        os.path.join(pkg2.prefix, 'example/pkg-1.2')]
    assert pkg2.path_list('long_version_path_list')  == [
        os.path.join(pkg2.prefix, 'example/pkg-1.2.0')]

    assert pkg1.path_list('short_version_path_list') == [
        os.path.join(pkg1.prefix, 'example/pkg-1.1')]
    assert pkg1.path_list('long_version_path_list')  == [
        os.path.join(pkg1.prefix, 'example/pkg-1.1.0')]


def test_path_list_pathattr(builtin_mock, config):
    spec = Spec('has-path-attr').concretized()
    pkg = spack.repo.get(spec)

    assert pkg.path_list('subdir_list_path_list') == [
        os.path.join(pkg.prefix, 'lib64'),
        os.path.join(pkg.prefix, 'lib/hasattr-1.3.0')]

    assert pkg.path_list('plain_list_path_list') == [
        os.path.join(pkg.prefix, 'lib64'),
        os.path.join(pkg.prefix, 'lib')]
