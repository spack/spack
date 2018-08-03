##############################################################################
# Copyright (c) 2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://software.llnl.gov/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.util.package_hash import package_hash, package_content
from spack.spec import Spec


def test_hash(tmpdir, mock_packages, config):
    package_hash("hash-test1@1.2")


def test_different_variants(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.2 +variantx")
    spec2 = Spec("hash-test1@1.2 +varianty")
    assert package_hash(spec1) == package_hash(spec2)


def test_all_same_but_name(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.2")
    spec2 = Spec("hash-test2@1.2")
    compare_sans_name(True, spec1, spec2)

    spec1 = Spec("hash-test1@1.2 +varianty")
    spec2 = Spec("hash-test2@1.2 +varianty")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_archive_hash(tmpdir, mock_packages, config):
    """
    Archive hash is not intended to be reflected in Package hash.
    """
    spec1 = Spec("hash-test1@1.3")
    spec2 = Spec("hash-test2@1.3")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patch_contents(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.1")
    spec2 = Spec("hash-test2@1.1")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_patches_to_apply(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.4")
    spec2 = Spec("hash-test2@1.4")
    compare_sans_name(True, spec1, spec2)


def test_all_same_but_install(tmpdir, mock_packages, config):
    spec1 = Spec("hash-test1@1.5")
    spec2 = Spec("hash-test2@1.5")
    compare_sans_name(False, spec1, spec2)


def compare_sans_name(eq, spec1, spec2):
    content1 = package_content(spec1)
    content1 = content1.replace(spec1.package.__class__.__name__, '')
    content2 = package_content(spec2)
    content2 = content2.replace(spec2.package.__class__.__name__, '')
    if eq:
        assert content1 == content2
    else:
        assert content1 != content2
