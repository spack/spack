# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import pytest

import spack.concretize
import spack.main
import spack.modules.lmod
from spack.config import Configuration
from spack.old_installer import PackageInstaller

module = spack.main.SpackCommand("module")

pytestmark = pytest.mark.not_on_windows("does not run on windows")

writer_cls = spack.modules.lmod.LmodModulefileWriter


@pytest.mark.db
def test_find_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    module("lmod", "find", "-r", "mpileaks ^mpich")


@pytest.mark.db
def test_loads_recursive_excluded(mutable_database, module_configuration):
    module_configuration("exclude")

    module("lmod", "refresh", "-y", "--delete-tree")
    output = module("lmod", "loads", "-r", "mpileaks ^mpich")
    lines = output.split("\n")

    assert any(re.match(r"[^#]*module load.*mpileaks", ln) for ln in lines)
    assert not any(re.match(r"[^#]module load.*callpath", ln) for ln in lines)
    assert any(re.match(r"## excluded or missing.*callpath", ln) for ln in lines)

    # TODO: currently there is no way to separate stdout and stderr when
    # invoking a SpackCommand. Supporting this requires refactoring
    # SpackCommand, or log_output, or both.
    # start_of_warning = spack.cmd.modules._missing_modules_warning[:10]
    # assert start_of_warning not in output


@pytest.mark.db
def test_setdefault_command(mutable_database, mutable_config: Configuration):
    data = {
        "default": {
            "enable": ["lmod"],
            "lmod": {"core_compilers": ["clang@3.3"], "hierarchy": ["mpi"]},
        }
    }
    mutable_config.set("modules", data)
    # Install two different versions of pkg-a
    other_spec, preferred = "pkg-a@1.0", "pkg-a@2.0"

    specs = [
        spack.concretize.concretize_one(other_spec),
        spack.concretize.concretize_one(preferred),
    ]
    PackageInstaller([s.package for s in specs], explicit=True, fake=True).install()

    writers = {
        preferred: writer_cls.from_spec(specs[1], "default"),
        other_spec: writer_cls.from_spec(specs[0], "default"),
    }

    # Create two module files for the same software
    module("lmod", "refresh", "-y", "--delete-tree", preferred, other_spec)

    # Assert initial directory state: no link and all module files present
    link_name = os.path.join(os.path.dirname(writers[preferred].layout.filename), "default")
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert not os.path.exists(link_name)

    # Set the default to be the other spec
    module("lmod", "setdefault", other_spec)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[other_spec].layout.filename)

    # Reset the default to be the preferred spec
    module("lmod", "setdefault", preferred)

    # Check that a link named 'default' exists, and points to the right file
    for k in preferred, other_spec:
        assert os.path.exists(writers[k].layout.filename)
    assert os.path.exists(link_name) and os.path.islink(link_name)
    assert os.path.realpath(link_name) == os.path.realpath(writers[preferred].layout.filename)
