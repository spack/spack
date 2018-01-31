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
import os

import spack
from spack.compiler import _parse_implicit_link_paths

#: directory with sample compiler data
datadir = os.path.join(spack.test_path, 'data', 'compiler_verbose_output')


def check_link_paths(filename, paths):
    with open(os.path.join(datadir, filename)) as file:
        output = file.read()
    detected_paths = _parse_implicit_link_paths(output)

    actual = set(detected_paths)
    expected = set(paths)

    missing_paths = expected - actual
    assert set() == missing_paths

    extra_paths = actual - expected
    assert set() == extra_paths


def test_icc16_link_paths():
    check_link_paths('icc-16.0.3.txt', [
        '/usr/lib64',
        '/usr/tce/packages/gcc/gcc-4.9.3/lib64',
        '/usr/tce/packages/intel/intel-16.0.3/compilers_and_libraries_2016.3.210/linux/compiler/lib/intel64_lin',  # noqa
        '/usr/lib',
        '/lib64',
        '/lib',
        '/usr/tce/packages/gcc/gcc-4.9.3/lib64/gcc/x86_64-unknown-linux-gnu/4.9.3'])  # noqa


def test_pgi_link_paths():
    check_link_paths('pgcc-16.3.txt', [
        '/usr/lib/gcc/x86_64-redhat-linux/4.8.5',
        '/usr/lib64',
        '/usr/tce/packages/pgi/pgi-16.3/linux86-64/16.3/lib'])


def test_gcc7_link_paths():
    check_link_paths('gcc-7.3.1.txt', [
        '/usr/lib/gcc/x86_64-redhat-linux/7',
        '/usr/lib64',
        '/lib64',
        '/usr/lib'])


def test_clang4_link_paths():
    check_link_paths('clang-4.0.1.txt', [
        '/usr/lib/gcc/x86_64-redhat-linux/7',
        '/usr/lib64',
        '/lib64',
        '/lib',
        '/usr/lib'])


def test_xl_link_paths():
    check_link_paths('xl-13.1.5.txt', [
        '/lib64',
        '/opt/ibm/xlC/13.1.5/lib',
        '/opt/ibm/xlmass/8.1.5/lib',
        '/opt/ibm/xlsmp/4.1.5/lib',
        '/usr/lib',
        '/usr/lib/gcc/ppc64le-redhat-linux/4.8.5',
        '/usr/lib64'])


def test_cce_link_paths():
    check_link_paths('cce-8.6.5.txt', [
        '/lib64',
        '/opt/cray/alps/6.5.28-6.0.5.0_18.6__g13a91b6.ari/lib64',
        '/opt/cray/dmapp/7.1.1-6.0.5.0_49.8__g1125556.ari/lib64',
        '/opt/cray/dmapp/default/lib64',
        '/opt/cray/pe/atp/2.1.1/libApp',
        '/opt/cray/pe/cce/8.6.5/binutils/x86_64/x86_64-unknown-linux-gnu/lib',
        '/opt/cray/pe/cce/8.6.5/cce/x86_64/lib',
        '/opt/cray/pe/libsci/17.12.1/CRAY/8.6/x86_64/lib',
        '/opt/cray/pe/mpt/7.7.0/gni/mpich-cray/8.6/lib',
        '/opt/cray/pe/pmi/5.0.13/lib64',
        '/opt/cray/rca/2.2.16-6.0.5.0_15.34__g5e09e6d.ari/lib64',
        '/opt/cray/udreg/2.3.2-6.0.5.0_13.12__ga14955a.ari/lib64',
        '/opt/cray/ugni/6.0.14-6.0.5.0_16.9__g19583bb.ari/lib64',
        '/opt/cray/wlm_detect/1.3.2-6.0.5.0_3.1__g388ccd5.ari/lib64',
        '/opt/cray/xpmem/2.2.4-6.0.5.0_4.8__g35d5e73.ari/lib64',
        '/opt/gcc/6.1.0/snos/lib/gcc/x86_64-suse-linux/6.1.0',
        '/opt/gcc/6.1.0/snos/lib64',
        '/usr/lib64'])
