##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
import sys
import filecmp
import pytest

from llnl.util.filesystem import working_dir, mkdirp

import spack.paths
import spack.util.compression
from spack.util.executable import Executable
from spack.stage import Stage
from spack.spec import Spec


@pytest.fixture()
def mock_stage(tmpdir, monkeypatch):
    # don't disrupt the spack install directory with tests.
    mock_path = str(tmpdir)
    monkeypatch.setattr(spack.paths, 'stage_path', mock_path)
    return mock_path


data_path = os.path.join(spack.paths.test_path, 'data', 'patch')


@pytest.mark.parametrize('filename, sha256, archive_sha256', [
    # compressed patch -- needs sha256 and archive_256
    (os.path.join(data_path, 'foo.tgz'),
     '252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
     '4e8092a161ec6c3a1b5253176fcf33ce7ba23ee2ff27c75dbced589dabacd06e'),
    # uncompressed patch -- needs only sha256
    (os.path.join(data_path, 'foo.patch'),
     '252c0af58be3d90e5dc5e0d16658434c9efa5d20a5df6c10bf72c2d77f780866',
     None)
])
def test_url_patch(mock_stage, filename, sha256, archive_sha256):
    # Make a patch object
    url = 'file://' + filename
    m = sys.modules['spack.patch']
    patch = m.Patch.create(
        None, url, sha256=sha256, archive_sha256=archive_sha256)

    # make a stage
    with Stage(url) as stage:  # TODO: url isn't used; maybe refactor Stage
        # TODO: there is probably a better way to mock this.
        stage.mirror_path = mock_stage  # don't disrupt the spack install

        # fake a source path
        with working_dir(stage.path):
            mkdirp('spack-expanded-archive')

        with working_dir(stage.source_path):
            # write a file to be patched
            with open('foo.txt', 'w') as f:
                f.write("""\
first line
second line
""")
            # write the expected result of patching.
            with open('foo-expected.txt', 'w') as f:
                f.write("""\
zeroth line
first line
third line
""")
        # apply the patch and compare files
        patch.apply(stage)

        with working_dir(stage.source_path):
            assert filecmp.cmp('foo.txt', 'foo-expected.txt')


def test_patch_in_spec(mock_packages, config):
    """Test whether patches in a package appear in the spec."""
    spec = Spec('patch')
    spec.concretize()
    assert 'patches' in list(spec.variants.keys())

    # Here the order is bar, foo, baz. Note that MV variants order
    # lexicographically based on the hash, not on the position of the
    # patch directive.
    assert (('7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730',
             'b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c',
             'bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c') ==
            spec.variants['patches'].value)


def test_patched_dependency(
        mock_packages, config, install_mockery, mock_fetch):
    """Test whether patched dependencies work."""
    spec = Spec('patch-a-dependency')
    spec.concretize()
    assert 'patches' in list(spec['libelf'].variants.keys())

    # make sure the patch makes it into the dependency spec
    assert (('c45c1564f70def3fc1a6e22139f62cb21cd190cc3a7dbe6f4120fa59ce33dcb8',) ==
            spec['libelf'].variants['patches'].value)

    # make sure the patch in the dependent's directory is applied to the
    # dependency
    libelf = spec['libelf']
    pkg = libelf.package
    pkg.do_patch()
    with pkg.stage:
        with working_dir(pkg.stage.source_path):
            # output a Makefile with 'echo Patched!' as the default target
            configure = Executable('./configure')
            configure()

            # Make sure the Makefile contains the patched text
            with open('Makefile') as mf:
                assert 'Patched!' in mf.read()


def test_multiple_patched_dependencies(mock_packages, config):
    """Test whether multiple patched dependencies work."""
    spec = Spec('patch-several-dependencies')
    spec.concretize()

    # basic patch on libelf
    assert 'patches' in list(spec['libelf'].variants.keys())
    # foo
    assert (('b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c',) ==
            spec['libelf'].variants['patches'].value)

    # URL patches
    assert 'patches' in list(spec['fake'].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (('1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd',
             'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234') ==
            spec['fake'].variants['patches'].value)


def test_conditional_patched_dependencies(mock_packages, config):
    """Test whether conditional patched dependencies work."""
    spec = Spec('patch-several-dependencies @1.0')
    spec.concretize()

    # basic patch on libelf
    assert 'patches' in list(spec['libelf'].variants.keys())
    # foo
    assert (('b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c',) ==
            spec['libelf'].variants['patches'].value)

    # conditional patch on libdwarf
    assert 'patches' in list(spec['libdwarf'].variants.keys())
    # bar
    assert (('7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730',) ==
            spec['libdwarf'].variants['patches'].value)
    # baz is conditional on libdwarf version
    assert ('bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c'
            not in spec['libdwarf'].variants['patches'].value)

    # URL patches
    assert 'patches' in list(spec['fake'].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (('1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd',
             'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234') ==
            spec['fake'].variants['patches'].value)


def test_conditional_patched_deps_with_conditions(mock_packages, config):
    """Test whether conditional patched dependencies with conditions work."""
    spec = Spec('patch-several-dependencies @1.0 ^libdwarf@20111030')
    spec.concretize()

    # basic patch on libelf
    assert 'patches' in list(spec['libelf'].variants.keys())
    # foo
    assert ('b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c'
            in spec['libelf'].variants['patches'].value)

    # conditional patch on libdwarf
    assert 'patches' in list(spec['libdwarf'].variants.keys())
    # bar
    assert ('7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730'
            in spec['libdwarf'].variants['patches'].value)
    # baz is conditional on libdwarf version (no guarantee on order w/conds)
    assert ('bf07a7fbb825fc0aae7bf4a1177b2b31fcf8a3feeaf7092761e18c859ee52a9c'
            in spec['libdwarf'].variants['patches'].value)

    # URL patches
    assert 'patches' in list(spec['fake'].variants.keys())
    # urlpatch.patch, urlpatch.patch.gz
    assert (('1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd',
             'abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234') ==
            spec['fake'].variants['patches'].value)
