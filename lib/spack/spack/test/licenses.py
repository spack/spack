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
# --- #
"""This test does checks the license text on all files in spack to be 
identical to this one here."""

import inspect
import os

import spack
import llnl.util.tty as tty


thisfile = inspect.getfile(inspect.currentframe())
with open(thisfile, 'r') as f:
    license = f.read().split('# --- #')[0]


def check_license(filepath):
    with open(filepath, 'r') as f:
        return f.read().startswith(license)


def test_check_licenses_lib():
    """Check the licenses in all spack files"""
    spack_lib_root = os.path.dirname(inspect.getfile(spack))
    failed_licenses = []
    for root, _, filenames in os.walk(spack_lib_root):
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                if not check_license(filepath):
                    failed_licenses.append(filepath)
    for fl in failed_licenses:
        tty.msg("{0:} has a changed license, compared to {1:}"
                "".format(fl, thisfile))
    assert failed_licenses == []


def test_check_licenses_package():
    """Check the licenses in all packages"""
    failed_licenses = []
    for name in spack.repo.all_package_names():
        if not check_license(spack.repo.filename_for_package_name(name)):
            failed_licenses.append(spack.repo.filename_for_package_name(name))
    for fl in failed_licenses:
        tty.msg("{0:} has a changed license, compared to {1:}"
                "".format(fl, thisfile))
    assert failed_licenses == []
