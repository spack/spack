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
import spack.modules
import spack.spec

lmod = spack.main.SpackCommand('lmod')

# Needed to make the fixture work
writer_cls = spack.modules.lmod.LmodModulefileWriter

# TODO : add tests for loads and find to check the prompt format


@pytest.fixture(
    params=[
        ['rm', 'doesnotexist'],  # Try to remove a non existing module
        ['find', 'mpileaks'],  # Try to find a module with multiple matches
        ['find', 'doesnotexist'],  # Try to find a module with no matches
    ]
)
def failure_args(request):
    """A list of arguments that will cause a failure"""
    return request.param


def test_exit_with_failure(database, failure_args):
    with pytest.raises(spack.main.SpackCommandError):
        lmod(*failure_args)


def test_setdefault_command(
        mutable_database, module_configuration
):

    module_configuration('autoload_direct')

    # Install two different versions of a package
    other_spec, preferred = 'a@1.0', 'a@2.0'

    spack.spec.Spec(other_spec).concretized().package.do_install(fake=True)
    spack.spec.Spec(preferred).concretized().package.do_install(fake=True)

    writers = {
        preferred: writer_cls(spack.spec.Spec(preferred).concretized()),
        other_spec: writer_cls(spack.spec.Spec(other_spec).concretized())
    }

    # Create two module files for the same software
    lmod('refresh', '-y', '--delete-tree', preferred, other_spec)

    # Assert initial directory state: no link and all module files present
    link_name = os.path.join(
        os.path.dirname(writers[preferred].layout.filename),
        'default'
    )
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert not os.path.exists(link_name)

    # Set the default to be the other spec
    lmod('setdefault', other_spec)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == writers[other_spec].layout.filename

    # Reset the default to be the preferred spec
    lmod('setdefault', preferred)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == writers[preferred].layout.filename
