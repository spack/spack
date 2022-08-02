# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks the binary packaging infrastructure
"""
import argparse
import os
import platform
import re
import shutil
import stat
import sys

import pytest

from llnl.util.filesystem import mkdirp
from llnl.util.symlink import symlink

import spack.binary_distribution as bindist
import spack.cmd.buildcache as buildcache
import spack.package_base
import spack.repo
import spack.store
import spack.util.gpg
from spack.fetch_strategy import FetchStrategyComposite, URLFetchStrategy
from spack.paths import mock_gpg_keys_path
from spack.relocate import (
    _placeholder,
    file_is_relocatable,
    macho_find_paths,
    macho_make_paths_normal,
    macho_make_paths_relative,
    needs_binary_relocation,
    needs_text_relocation,
    relocate_links,
    relocate_text,
)
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32",
                                reason="does not run on windows")


def fake_fetchify(url, pkg):
    """Fake the URL for a package so it downloads from a file."""
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(url))
    pkg.fetcher = fetcher


@pytest.mark.usefixtures('install_mockery', 'mock_gnupghome')
def test_buildcache(mock_archive, tmpdir):
    # tweak patchelf to only do a download
    pspec = Spec("patchelf")
    pspec.concretize()
    pkg = spack.repo.get(pspec)
    fake_fetchify(pkg.fetcher, pkg)
    mkdirp(pkg.prefix.joinpath( "bin"))
    patchelfscr = pkg.prefix.joinpath( "bin", "patchelf")
    f = open(patchelfscr, 'w')
    body = """#!/bin/bash
echo $PATH"""
    f.write(body)
    f.close()
    st = patchelfscr.stat()
    patchelfscr.chmod(st.st_mode | stat.S_IEXEC)

    # Install the test package
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    pkg = spec.package
    fake_fetchify(mock_archive.url, pkg)
    pkg.do_install()
    pkghash = '/' + str(spec.dag_hash(7))

    # Put some non-relocatable file in there
    filename = spec.prefix.joinpath( "dummy.txt")
    with open(filename, "w") as script:
        script.write(spec.prefix)

    # Create an absolute symlink
    linkname = spec.prefix.joinpath( "link_to_dummy.txt")
    symlink(filename, linkname)

    # Create the build cache  and
    # put it directly into the mirror
    mirror_path = str(tmpdir).joinpath( 'test-mirror')
    spack.mirror.create(mirror_path, specs=[])

    # register mirror with spack config
    mirrors = {'spack-mirror-test': 'file://' + mirror_path}
    spack.config.set('mirrors', mirrors)

    stage = spack.stage.Stage(
        mirrors['spack-mirror-test'], name="build_cache", keep=True)
    stage.create()

    # setup argument parser
    parser = argparse.ArgumentParser()
    buildcache.setup_parser(parser)

    create_args = ['create', '-a', '-f', '-d', mirror_path, pkghash]
    # Create a private key to sign package with if gpg2 available
    spack.util.gpg.create(name='test key 1', expires='0',
                          email='spack@googlegroups.com',
                          comment='Spack test key')

    create_args.insert(create_args.index('-a'), '--rebuild-index')

    args = parser.parse_args(create_args)
    buildcache.buildcache(parser, args)
    # trigger overwrite warning
    buildcache.buildcache(parser, args)

    # Uninstall the package
    pkg.do_uninstall(force=True)

    install_args = ['install', '-a', '-f', pkghash]
    args = parser.parse_args(install_args)
    # Test install
    buildcache.buildcache(parser, args)

    files = os.listdir(spec.prefix)

    assert 'link_to_dummy.txt' in files
    assert 'dummy.txt' in files

    # Validate the relocation information
    buildinfo = bindist.read_buildinfo_file(spec.prefix)
    assert(buildinfo['relocate_textfiles'] == ['dummy.txt'])
    assert(buildinfo['relocate_links'] == ['link_to_dummy.txt'])

    # create build cache with relative path
    create_args.insert(create_args.index('-a'), '-f')
    create_args.insert(create_args.index('-a'), '-r')
    args = parser.parse_args(create_args)
    buildcache.buildcache(parser, args)

    # Uninstall the package
    pkg.do_uninstall(force=True)

    args = parser.parse_args(install_args)
    buildcache.buildcache(parser, args)

    # test overwrite install
    install_args.insert(install_args.index('-a'), '-f')
    args = parser.parse_args(install_args)
    buildcache.buildcache(parser, args)

    files = os.listdir(spec.prefix)
    assert 'link_to_dummy.txt' in files
    assert 'dummy.txt' in files
#    assert os.path.realpath(
#        spec.prefix.joinpath( 'link_to_dummy.txt')
#    ) == os.path.realpath(spec.prefix.joinpath( 'dummy.txt'))

    args = parser.parse_args(['keys'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['list', 'trivial'])
    buildcache.buildcache(parser, args)

    # Copy a key to the mirror to have something to download
    shutil.copyfile(mock_gpg_keys_path + '/external.key',
                    mirror_path + '/external.key')

    args = parser.parse_args(['keys'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['keys', '-f'])
    buildcache.buildcache(parser, args)

    args = parser.parse_args(['keys', '-i', '-t'])
    buildcache.buildcache(parser, args)

    # unregister mirror with spack config
    mirrors = {}
    spack.config.set('mirrors', mirrors)
    shutil.rmtree(mirror_path)
    stage.destroy()

    # Remove cached binary specs since we deleted the mirror
    bindist._cached_specs = set()


@pytest.mark.usefixtures('install_mockery')
def test_relocate_text(tmpdir):
    spec = Spec('trivial-install-test-package')
    spec.concretize()
    with tmpdir.as_cwd():
        # Validate the text path replacement
        old_dir = '/home/spack/opt/spack'
        filename = 'dummy.txt'
        with open(filename, "w") as script:
            script.write(old_dir)
            script.close()
        filenames = [filename]
        new_dir = '/opt/rh/devtoolset/'
        # Singleton dict doesn't matter if Ordered
        relocate_text(filenames, {old_dir: new_dir})
        with open(filename, "r")as script:
            for line in script:
                assert(new_dir in line)
        assert(file_is_relocatable(os.path.realpath(filename)))
    # Remove cached binary specs since we deleted the mirror
    bindist._cached_specs = set()


def test_relocate_links(tmpdir):
    with tmpdir.as_cwd():
        old_layout_root = os.path.join(
            '%s' % tmpdir, 'home', 'spack', 'opt', 'spack')
        old_install_prefix = os.path.join(
            '%s' % old_layout_root, 'debian6', 'test')
        old_binname = old_install_prefix.joinpath( 'binfile')
        placeholder = _placeholder(old_layout_root)
        re.sub(old_layout_root, placeholder, old_binname)
        filenames = ['link.ln', 'outsideprefix.ln']
        new_layout_root = os.path.join(
            '%s' % tmpdir, 'opt', 'rh', 'devtoolset')
        new_install_prefix = os.path.join(
            '%s' % new_layout_root, 'test', 'debian6')
        new_linkname = new_install_prefix.joinpath( 'link.ln')
        new_linkname2 = new_install_prefix.joinpath( 'outsideprefix.ln')
        new_binname = new_install_prefix.joinpath( 'binfile')
        mkdirp(new_install_prefix)
        with open(new_binname, 'w') as f:
            f.write('\n')
        os.utime(new_binname, None)
        symlink(old_binname, new_linkname)
        symlink('/usr/lib/libc.so', new_linkname2)
        relocate_links(filenames, old_layout_root,
                       old_install_prefix, new_install_prefix)
        assert os.readlink(new_linkname) == new_binname
        assert os.readlink(new_linkname2) == '/usr/lib/libc.so'


def test_needs_relocation():

    assert needs_binary_relocation('application', 'x-sharedlib')
    assert needs_binary_relocation('application', 'x-executable')
    assert not needs_binary_relocation('application', 'x-octet-stream')
    assert not needs_binary_relocation('text', 'x-')
    assert needs_text_relocation('text', 'x-')
    assert not needs_text_relocation('symbolic link to', 'x-')

    assert needs_binary_relocation('application', 'x-mach-binary')


def test_replace_paths(tmpdir):
    with tmpdir.as_cwd():
        suffix = 'dylib' if platform.system().lower() == 'darwin' else 'so'
        hash_a = '53moz6jwnw3xpiztxwhc4us26klribws'
        hash_b = 'tk62dzu62kd4oh3h3heelyw23hw2sfee'
        hash_c = 'hdkhduizmaddpog6ewdradpobnbjwsjl'
        hash_d = 'hukkosc7ahff7o65h6cdhvcoxm57d4bw'
        hash_loco = 'zy4oigsc4eovn5yhr2lk4aukwzoespob'

        prefix2hash = dict()

        old_spack_dir = '%s' % tmpdir.joinpath(
                                     'Users', 'developer', 'spack')
        mkdirp(old_spack_dir)

        oldprefix_a = '%s' % old_spack_dir.joinpath( 'pkgA-%s' % hash_a)
        oldlibdir_a = '%s' % oldprefix_a.joinpath( 'lib')
        mkdirp(oldlibdir_a)
        prefix2hash[str(oldprefix_a)] = hash_a

        oldprefix_b = '%s' % old_spack_dir.joinpath( 'pkgB-%s' % hash_b)
        oldlibdir_b = '%s' % oldprefix_b.joinpath( 'lib')
        mkdirp(oldlibdir_b)
        prefix2hash[str(oldprefix_b)] = hash_b

        oldprefix_c = '%s' % old_spack_dir.joinpath( 'pkgC-%s' % hash_c)
        oldlibdir_c = '%s' % oldprefix_c.joinpath( 'lib')
        oldlibdir_cc = '%s' % oldlibdir_c.joinpath( 'C')
        mkdirp(oldlibdir_c)
        prefix2hash[str(oldprefix_c)] = hash_c

        oldprefix_d = '%s' % old_spack_dir.joinpath( 'pkgD-%s' % hash_d)
        oldlibdir_d = '%s' % oldprefix_d.joinpath( 'lib')
        mkdirp(oldlibdir_d)
        prefix2hash[str(oldprefix_d)] = hash_d

        oldprefix_local = Path('%s' % tmpdir, 'usr').joinpath( 'local')
        oldlibdir_local = '%s' % oldprefix_local.joinpath( 'lib')
        mkdirp(oldlibdir_local)
        prefix2hash[str(oldprefix_local)] = hash_loco
        libfile_a = 'libA.%s' % suffix
        libfile_b = 'libB.%s' % suffix
        libfile_c = 'libC.%s' % suffix
        libfile_d = 'libD.%s' % suffix
        libfile_loco = 'libloco.%s' % suffix
        old_libnames  = [oldlibdir_a.joinpath( libfile_a),
                         oldlibdir_b.joinpath( libfile_b),
                         oldlibdir_c.joinpath( libfile_c),
                         oldlibdir_d.joinpath( libfile_d),
                         oldlibdir_local.joinpath( libfile_loco)]

        for old_libname in old_libnames:
            with open(old_libname, 'a'):
                os.utime(old_libname, None)

        hash2prefix = dict()

        new_spack_dir = '%s' % tmpdir.joinpath( 'Users', 'Shared',
                                     'spack')
        mkdirp(new_spack_dir)

        prefix_a = new_spack_dir.joinpath( 'pkgA-%s' % hash_a)
        libdir_a = prefix_a.joinpath( 'lib')
        mkdirp(libdir_a)
        hash2prefix[hash_a] = str(prefix_a)

        prefix_b = new_spack_dir.joinpath( 'pkgB-%s' % hash_b)
        libdir_b = prefix_b.joinpath( 'lib')
        mkdirp(libdir_b)
        hash2prefix[hash_b] = str(prefix_b)

        prefix_c = new_spack_dir.joinpath( 'pkgC-%s' % hash_c)
        libdir_c = prefix_c.joinpath( 'lib')
        libdir_cc = libdir_c.joinpath( 'C')
        mkdirp(libdir_cc)
        hash2prefix[hash_c] = str(prefix_c)

        prefix_d = new_spack_dir.joinpath( 'pkgD-%s' % hash_d)
        libdir_d = prefix_d.joinpath( 'lib')
        mkdirp(libdir_d)
        hash2prefix[hash_d] = str(prefix_d)

        prefix_local = Path('%s' % tmpdir, 'usr').joinpath( 'local')
        libdir_local = prefix_local.joinpath( 'lib')
        mkdirp(libdir_local)
        hash2prefix[hash_loco] = str(prefix_local)

        new_libnames  = [libdir_a.joinpath( libfile_a),
                         libdir_b.joinpath( libfile_b),
                         libdir_cc.joinpath( libfile_c),
                         libdir_d.joinpath( libfile_d),
                         libdir_local.joinpath( libfile_loco)]

        for new_libname in new_libnames:
            with open(new_libname, 'a'):
                os.utime(new_libname, None)

        prefix2prefix = dict()
        for prefix, hash in prefix2hash.items():
            prefix2prefix[prefix] = hash2prefix[hash]

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c,
                                     oldlibdir_cc, oldlibdir_local],
                                    [oldlibdir_a.joinpath(
                                                  libfile_a),oldlibdir_a.joinpath(
                                                  libfile_a)b,oldlibdir_a.joinpath(
                                                  libfile_a)oldlibdir_a.joinpath(
                                                  libfile_a)_local,
                                                  libfile_loco)],
                                    os.path.join(oldlibdir_cc,
                                                 libfile_c),
                                    old_spack_dir,
                                    prefix2prefix
                                    )
        assert out_dict == {oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            oldlibdir_a.joinpath( libfile_a):
                            libdir_a.joinpath( libfile_a),
                            oldlibdir_b.joinpath( libfile_b):
                            libdir_b.joinpath( libfile_b),
                            oldlibdir_local.joinpath( libfile_loco):
                            libdir_local.joinpath( libfile_loco),
                            oldlibdir_cc.joinpath( libfile_c):
                            libdir_cc.joinpath( libfile_c)}

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c,
                                     oldlibdir_cc,
                                     oldlibdir_local],
                                    [oldlibdir_a.joinpath(
                                                  libfile_a),oldlibdir_a.joinpath(
                                                  libfile_a)b,oldlibdir_a.joinpath(
                                                  libfile_a),oldlibdir_a.joinpath(
                                                  libfile_a)
                                                  libfile_c),
                                     os.path.join(oldlibdir_local,
                                                  libfile_loco)],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix
                                    )
        assert out_dict == {oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            oldlibdir_a.joinpath( libfile_a):
                            libdir_a.joinpath( libfile_a),
                            oldlibdir_b.joinpath( libfile_b):
                            libdir_b.joinpath( libfile_b),
                            oldlibdir_local.joinpath( libfile_loco):
                            libdir_local.joinpath( libfile_loco),
                            oldlibdir_cc.joinpath( libfile_c):
                            libdir_cc.joinpath( libfile_c)}

        out_dict = macho_find_paths([oldlibdir_a, oldlibdir_b,
                                     oldlibdir_c, oldlibdir_cc,
                                     oldlibdir_local],
                                    ['@rpath/%s' % libfile_a,
                                     '@rpath/%s' % libfile_b,
                                     '@rpath/%s' % libfile_c,
                                     '@rpath/%s' % libfile_loco],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix
                                    )

        assert out_dict == {'@rpath/%s' % libfile_a:
                            '@rpath/%s' % libfile_a,
                            '@rpath/%s' % libfile_b:
                            '@rpath/%s' % libfile_b,
                            '@rpath/%s' % libfile_c:
                            '@rpath/%s' % libfile_c,
                            '@rpath/%s' % libfile_loco:
                            '@rpath/%s' % libfile_loco,
                            oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_c: libdir_c,
                            oldlibdir_cc: libdir_cc,
                            libdir_local: libdir_local,
                            }

        out_dict = macho_find_paths([oldlibdir_a,
                                     oldlibdir_b,
                                     oldlibdir_d,
                                     oldlibdir_local],
                                    ['@rpath/%s' % libfile_a,
                                     '@rpath/%s' % libfile_b,
                                     '@rpath/%s' % libfile_loco],
                                    None,
                                    old_spack_dir,
                                    prefix2prefix)
        assert out_dict == {'@rpath/%s' % libfile_a:
                            '@rpath/%s' % libfile_a,
                            '@rpath/%s' % libfile_b:
                            '@rpath/%s' % libfile_b,
                            '@rpath/%s' % libfile_loco:
                            '@rpath/%s' % libfile_loco,
                            oldlibdir_a: libdir_a,
                            oldlibdir_b: libdir_b,
                            oldlibdir_d: libdir_d,
                            libdir_local: libdir_local,
                            }


def test_macho_make_paths():
    out = macho_make_paths_relative('/Users/Shared/spack/pkgC/lib/libC.dylib',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'),
                                    '/Users/Shared/spack/pkgC/lib/libC.dylib')
    assert out == {'/Users/Shared/spack/pkgA/lib':
                   '@loader_path/../../pkgA/lib',
                   '/Users/Shared/spack/pkgB/lib':
                   '@loader_path/../../pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '/Users/Shared/spack/pkgA/libA.dylib':
                   '@loader_path/../../pkgA/libA.dylib',
                   '/Users/Shared/spack/pkgB/libB.dylib':
                   '@loader_path/../../pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib',
                   '/Users/Shared/spack/pkgC/lib/libC.dylib':
                   '@rpath/libC.dylib'}

    out = macho_make_paths_normal('/Users/Shared/spack/pkgC/lib/libC.dylib',
                                  ('@loader_path/../../pkgA/lib',
                                   '@loader_path/../../pkgB/lib',
                                   '/usr/local/lib'),
                                  ('@loader_path/../../pkgA/libA.dylib',
                                   '@loader_path/../../pkgB/libB.dylib',
                                   '/usr/local/lib/libloco.dylib'),
                                  '@rpath/libC.dylib')

    assert out == {'@rpath/libC.dylib':
                   '/Users/Shared/spack/pkgC/lib/libC.dylib',
                   '@loader_path/../../pkgA/lib':
                   '/Users/Shared/spack/pkgA/lib',
                   '@loader_path/../../pkgB/lib':
                   '/Users/Shared/spack/pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '@loader_path/../../pkgA/libA.dylib':
                   '/Users/Shared/spack/pkgA/libA.dylib',
                   '@loader_path/../../pkgB/libB.dylib':
                   '/Users/Shared/spack/pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'
                   }

    out = macho_make_paths_relative('/Users/Shared/spack/pkgC/bin/exeC',
                                    '/Users/Shared/spack',
                                    ('/Users/Shared/spack/pkgA/lib',
                                     '/Users/Shared/spack/pkgB/lib',
                                     '/usr/local/lib'),
                                    ('/Users/Shared/spack/pkgA/libA.dylib',
                                     '/Users/Shared/spack/pkgB/libB.dylib',
                                     '/usr/local/lib/libloco.dylib'), None)

    assert out == {'/Users/Shared/spack/pkgA/lib':
                   '@loader_path/../../pkgA/lib',
                   '/Users/Shared/spack/pkgB/lib':
                   '@loader_path/../../pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '/Users/Shared/spack/pkgA/libA.dylib':
                   '@loader_path/../../pkgA/libA.dylib',
                   '/Users/Shared/spack/pkgB/libB.dylib':
                   '@loader_path/../../pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'}

    out = macho_make_paths_normal('/Users/Shared/spack/pkgC/bin/exeC',
                                  ('@loader_path/../../pkgA/lib',
                                   '@loader_path/../../pkgB/lib',
                                   '/usr/local/lib'),
                                  ('@loader_path/../../pkgA/libA.dylib',
                                      '@loader_path/../../pkgB/libB.dylib',
                                      '/usr/local/lib/libloco.dylib'),
                                  None)

    assert out == {'@loader_path/../../pkgA/lib':
                   '/Users/Shared/spack/pkgA/lib',
                   '@loader_path/../../pkgB/lib':
                   '/Users/Shared/spack/pkgB/lib',
                   '/usr/local/lib': '/usr/local/lib',
                   '@loader_path/../../pkgA/libA.dylib':
                   '/Users/Shared/spack/pkgA/libA.dylib',
                   '@loader_path/../../pkgB/libB.dylib':
                   '/Users/Shared/spack/pkgB/libB.dylib',
                   '/usr/local/lib/libloco.dylib':
                   '/usr/local/lib/libloco.dylib'}


@pytest.fixture()
def mock_download():
    """Mock a failing download strategy."""
    class FailedDownloadStrategy(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                "<non-existent URL>", "This FetchStrategy always fails")

    fetcher = FetchStrategyComposite()
    fetcher.append(FailedDownloadStrategy())

    @property
    def fake_fn(self):
        return fetcher

    orig_fn = spack.package_base.PackageBase.fetcher
    spack.package_base.PackageBase.fetcher = fake_fn
    yield
    spack.package_base.PackageBase.fetcher = orig_fn


@pytest.mark.parametrize("manual,instr", [(False, False), (False, True),
                                          (True, False), (True, True)])
@pytest.mark.disable_clean_stage_check
def test_manual_download(install_mockery, mock_download, monkeypatch, manual,
                         instr):
    """
    Ensure expected fetcher fail message based on manual download and instr.
    """
    @property
    def _instr(pkg):
        return 'Download instructions for {0}'.format(pkg.spec.name)

    spec = Spec('a').concretized()
    pkg = spec.package

    pkg.manual_download = manual
    if instr:
        monkeypatch.setattr(spack.package_base.PackageBase, 'download_instr',
                            _instr)

    expected = pkg.download_instr if manual else 'All fetchers failed'
    with pytest.raises(spack.fetch_strategy.FetchError, match=expected):
        pkg.do_fetch()


@pytest.fixture()
def fetching_not_allowed(monkeypatch):
    class FetchingNotAllowed(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise Exception("Sources are fetched but shouldn't have been")
    fetcher = FetchStrategyComposite()
    fetcher.append(FetchingNotAllowed())
    monkeypatch.setattr(spack.package_base.PackageBase, 'fetcher', fetcher)


def test_fetch_without_code_is_noop(install_mockery, fetching_not_allowed):
    """do_fetch for packages without code should be a no-op"""
    pkg = Spec('a').concretized().package
    pkg.has_code = False
    pkg.do_fetch()


def test_fetch_external_package_is_noop(install_mockery, fetching_not_allowed):
    """do_fetch for packages without code should be a no-op"""
    spec = Spec('a').concretized()
    spec.external_path = "/some/where"
    assert spec.external
    spec.package.do_fetch()
