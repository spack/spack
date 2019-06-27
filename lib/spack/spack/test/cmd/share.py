# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.config
import spack.error

from spack.main import SpackCommand

share = SpackCommand('share')
install = SpackCommand('install')


@pytest.fixture()
def local_tmpdir():
    print("We be making them tmpdirs")


def test_activate():
    share('activate')
    assert spack.config.get('config:shared') is True


def test_deactivate():
    # Ensures that this test can be run individually
    # Activates shared mode so shared mode can be deactivated
    if not spack.config.get('config:shared'):
        share('activate')
    share('deactivate')
    assert spack.config.get('config:shared') is False
