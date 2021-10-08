# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys
from typing import Dict  # novm

import pytest

from llnl.util.filesystem import working_dir

from spack.util import compression as scomp
from spack.util.executable import CommandNotFoundError, which


def compose_to_dict(pkg, ext, dict):
    dict[ext] = pkg
    return pkg


ext_archive = {}  # type: Dict[str, str]
fake_archives = [compose_to_dict('.'.join(['Foo', ext]), ext, ext_archive) for ext
                 in scomp.ALLOWED_ARCHIVE_TYPES]


def build_temp_archive(extension, mode, archiver, compression, archive_file, ext_dir):
    if compression.lower() == 'z':
        pytest.skip('Extension %s unsupported for testing')
    if compression in ['xz', 'txz']:
        try:
            import lzma  # noqa # novermin
        except ImportError:
            archiver = which('tar')
            archiver.add_default_arg('-cfFoo.%s' % extension)
            mode = 'system_tar'
    out = os.path.join(ext_dir, 'Foo.%s' % extension)
    if mode == 'tarfile':
        archive = archiver.open(out, 'w:%s' % compression)
        archive.add(archive_file)
        archive.close()
    elif mode == 'system_tar':
        with working_dir(ext_dir):
            archiver(os.path.basename(archive_file))
    else:
        zip = archiver.ZipFile(out, 'w')
        zip.write(archive_file)
        zip.close()


def derive_compression_algo(ext, style):
    native = style == 'native'
    if ext and re.match(r'\.?zip$', ext):
        return 'zipfile' if native else "unzip"
    if ext and re.match(r'gz', ext):
        return 'gzip' if native else "gzip"
    if ext and re.match(r'bz2', ext):
        return 'bz2' if native else "bunzip2"
    if ext and not re.search(r'\.?Z', ext):
        return 'tarfile' if native else "tar"


def is_on_system(util):
    return bool(which(util, required=False))


def module(ext, archiver=None):
    try:
        mod = __import__(ext)
        if archiver:
            archiver[0] = mod
    except ImportError:
        return False
    return True


def skip(extension, resource_type):
    if resource_type == "native":
        can_skip = module(derive_compression_algo(extension, resource_type))
    else:
        can_skip = is_on_system(derive_compression_algo(extension, resource_type))
    return can_skip


@pytest.fixture
def archive_file(tmpdir_factory, request):
    """ Creates a temporary directory containing a temp empty archive file"""
    extension = request.param
    mod = 'tarfile'
    archiver = [0]
    compression = extension.lower()
    decomp_ext = extension.split('.')
    if decomp_ext[1:]:
        compression = decomp_ext[-1]
    elif re.match('t', extension) and not re.match('tar', extension):
        compression = extension[1:]
        if extension[1:] == 'bz':
            compression = compression + '2'
    if extension == 'zip':
        mod = 'zipfile'
    if not module(mod, archiver):
        pytest.skip('Archiver Module not available')
    tmpdir = tmpdir_factory.mktemp('compression')
    test = tmpdir.mkdir('test')
    test_file = test / "comp.txt"
    test_file.write("Spack Compression Test")
    build_temp_archive(extension, mod, archiver[0], compression, str(test), str(tmpdir))
    return os.path.join(str(tmpdir), 'Foo.%s' % extension)


@pytest.mark.parametrize('archive_file', scomp.ALLOWED_ARCHIVE_TYPES, indirect=True)
def test_native_unpacking(tmpdir_factory, archive_file):
    extension = scomp.extension(archive_file)
    if not skip(extension, "native"):
        pytest.skip("Extension %s does not have native python\
        support on this system." % extension)
    util = scomp.decompressor_for(archive_file, extension)
    tmpdir = tmpdir_factory.mktemp("comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        assert os.listdir(os.getcwd())


@pytest.mark.parametrize('archive_file', scomp.ALLOWED_ARCHIVE_TYPES, indirect=True)
def test_system_unpacking(tmpdir_factory, archive_file):
    extension = scomp.extension(archive_file)
    if not skip(extension, "system"):
        pytest.fail("Extension %s does not have system support." % extension)
    # configure testing env, remove import resolution attributes
    tmp_path = sys.path
    catch_modules = sys.modules
    sys.path = []
    sys.modules = {}

    # actually run test
    util = scomp.decompressor_for(archive_file, extension)
    tmpdir = tmpdir_factory.mktemp("system_comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        assert os.listdir(os.getcwd())

    # restore system attributes
    sys.path = tmp_path
    sys.modules = catch_modules


def test_unallowed_extension():
    bad_ext_archive = 'Foo.py'
    with pytest.raises(CommandNotFoundError):
        scomp.decompressor_for(bad_ext_archive, 'py')


@pytest.mark.parametrize('archive', fake_archives)
def test_get_extension(archive):
    ext = scomp.extension(archive)
    assert ext_archive[ext] == archive


def test_get_bad_extension():
    archive = 'Foo.py'
    ext = scomp.extension(archive)
    assert ext is None


@pytest.mark.parametrize('path', fake_archives)
def test_allowed_archvie(path):
    assert scomp.allowed_archive(path)
