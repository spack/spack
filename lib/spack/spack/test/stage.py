# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test that the Stage class works correctly."""
import os
import collections
import shutil
import stat
import tempfile
import getpass

import pytest

from llnl.util.filesystem import mkdirp, working_dir

import spack.paths
import spack.stage
import spack.util.executable

from spack.resource import Resource
from spack.stage import Stage, StageComposite, ResourceStage, DIYStage
from spack.util.path import canonicalize_path

# The following values are used for common fetch and stage mocking fixtures:
_archive_base = 'test-files'
_archive_fn = '%s.tar.gz' % _archive_base
_extra_fn = 'extra.sh'
_hidden_fn = '.hidden'
_readme_fn = 'README.txt'

_extra_contents = '#!/bin/sh\n'
_hidden_contents = ''
_readme_contents = 'hello world!\n'

# TODO: Replace the following with an enum once guarantee supported (or
# include enum34 for python versions < 3.4.
_include_readme = 1
_include_hidden = 2
_include_extra = 3

# Some standard unix directory that does NOT include the username
_non_user_root = os.path.join(os.path.sep, 'opt')


# Mock fetch directories are expected to appear as follows:
#
# TMPDIR/
#     _archive_fn     archive_url = file:///path/to/_archive_fn
#
# Mock expanded stage directories are expected to have one of two forms,
# depending on how the tarball expands.  Non-exploding tarballs are expected
# to have the following structure:
#
# TMPDIR/                 temp stage dir
#     spack-src/          well-known stage source directory
#         _readme_fn      Optional test_readme (contains _readme_contents)
#     _hidden_fn          Optional hidden file (contains _hidden_contents)
#     _archive_fn         archive_url = file:///path/to/_archive_fn
#
# while exploding tarball directories are expected to be structured as follows:
#
# TMPDIR/                 temp stage dir
#     spack-src/          well-known stage source directory
#         archive_name/   archive dir
#             _readme_fn  test_readme (contains _readme_contents)
#         _extra_fn       test_extra file (contains _extra_contents)
#     _archive_fn         archive_url = file:///path/to/_archive_fn
#


def check_expand_archive(stage, stage_name, expected_file_list):
    """
    Ensure the expanded archive directory contains the expected structure and
    files as described in the module-level comments above.
    """
    stage_path = get_stage_path(stage, stage_name)
    archive_dir = spack.stage._source_path_subdir

    stage_contents = os.listdir(stage_path)
    assert _archive_fn in stage_contents
    assert archive_dir in stage_contents

    source_path = os.path.join(stage_path, archive_dir)
    assert source_path == stage.source_path

    source_contents = os.listdir(source_path)

    for _include in expected_file_list:
        if _include == _include_hidden:
            # The hidden file represent the HFS metadata associated with Mac
            # OS X tar files so is expected to be in the same directory as
            # the archive directory.
            assert _hidden_fn in stage_contents

            fn = os.path.join(stage_path, _hidden_fn)
            contents = _hidden_contents

        elif _include == _include_readme:
            # The standard README.txt file will be in the source directory if
            # the tarball didn't explode; otherwise, it will be in the
            # original archive subdirectory of it.
            if _archive_base in source_contents:
                fn = os.path.join(source_path, _archive_base, _readme_fn)
            else:
                fn = os.path.join(source_path, _readme_fn)
            contents = _readme_contents

        elif _include == _include_extra:
            assert _extra_fn in source_contents

            fn = os.path.join(source_path, _extra_fn)
            contents = _extra_contents

        else:
            assert False

        assert os.path.isfile(fn)
        with open(fn) as _file:
            _file.read() == contents


def check_fetch(stage, stage_name):
    """
    Ensure the fetch resulted in a properly placed archive file as described in
    the module-level comments.
    """
    stage_path = get_stage_path(stage, stage_name)
    assert _archive_fn in os.listdir(stage_path)
    assert os.path.join(stage_path, _archive_fn) == stage.fetcher.archive_file


def check_destroy(stage, stage_name):
    """Figure out whether a stage was destroyed correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # check that the stage dir/link was removed.
    assert not os.path.exists(stage_path)

    # tmp stage needs to remove tmp dir too.
    if not stage.managed_by_spack:
        target = os.path.realpath(stage_path)
        assert not os.path.exists(target)


def check_setup(stage, stage_name, archive):
    """Figure out whether a stage was set up correctly."""
    stage_path = get_stage_path(stage, stage_name)

    # Ensure stage was created in the spack stage directory
    assert os.path.isdir(stage_path)

    # Make sure it points to a valid directory
    target = os.path.realpath(stage_path)
    assert os.path.isdir(target)
    assert not os.path.islink(target)

    # Make sure the directory is in the place we asked it to
    # be (see setUp, tearDown, and use_tmp)
    assert target.startswith(str(archive.stage_path))


def get_stage_path(stage, stage_name):
    """Figure out where a stage should be living. This depends on
    whether it's named.
    """
    stage_path = spack.stage.get_stage_root()
    if stage_name is not None:
        # If it is a named stage, we know where the stage should be
        return os.path.join(stage_path, stage_name)
    else:
        # If it's unnamed, ensure that we ran mkdtemp in the right spot.
        assert stage.path is not None
        assert stage.path.startswith(stage_path)
        return stage.path


@pytest.fixture
def bad_stage_path():
    """Temporarily ensure there is no accessible path for staging."""
    current = spack.config.get('config:build_stage')
    spack.config.set('config', {'build_stage': '/no/such/path'}, scope='user')
    yield
    spack.config.set('config', {'build_stage': current}, scope='user')


@pytest.fixture
def non_user_path_for_stage(monkeypatch):
    """Temporarily use a Linux-standard non-user path for staging. """
    def _can_access(path, perms):
        return True

    current = spack.config.get('config:build_stage')
    spack.config.set('config', {'build_stage': [_non_user_root]}, scope='user')
    monkeypatch.setattr(os, 'access', _can_access)
    yield
    spack.config.set('config', {'build_stage': current}, scope='user')


@pytest.fixture
def instance_path_for_stage():
    """
    Temporarily use the "traditional" spack instance stage path for staging.

    Note that it can be important for other tests that the previous settings be
    restored when the test case is over.
    """
    current = spack.config.get('config:build_stage')
    base = canonicalize_path(os.path.join('$spack', 'test-stage'))
    mkdirp(base)
    path = tempfile.mkdtemp(dir=base)
    spack.config.set('config', {'build_stage': path}, scope='user')
    yield
    spack.config.set('config', {'build_stage': current}, scope='user')
    shutil.rmtree(base)


@pytest.fixture
def tmp_path_for_stage(tmpdir):
    """
    Use a temporary test directory for staging.

    Note that it can be important for other tests that the previous settings be
    restored when the test case is over.
    """
    current = spack.config.get('config:build_stage')
    spack.config.set('config', {'build_stage': [str(tmpdir)]}, scope='user')
    yield tmpdir
    spack.config.set('config', {'build_stage': current}, scope='user')


@pytest.fixture
def tmp_build_stage_dir(tmpdir):
    """Establish the temporary build_stage for the mock archive."""
    test_stage_path = tmpdir.join('stage')

    # Set test_stage_path as the default directory to use for test stages.
    current = spack.config.get('config:build_stage')
    spack.config.set('config',
                     {'build_stage': [str(test_stage_path)]}, scope='user')

    yield (tmpdir, test_stage_path)

    spack.config.set('config', {'build_stage': current}, scope='user')


@pytest.fixture
def mock_stage_archive(clear_stage_root, tmp_build_stage_dir, request):
    """
    Create the directories and files for the staged mock archive.

    Note that it can be important for other tests that the previous settings be
    restored when the test case is over.
    """
    # Mock up a stage area that looks like this:
    #
    # tmpdir/                test_files_dir
    #     stage/             test_stage_path (where stage should be)
    #     <_archive_base>/   archive_dir_path
    #         <_readme_fn>   Optional test_readme (contains _readme_contents)
    #     <_extra_fn>        Optional extra file (contains _extra_contents)
    #     <_hidden_fn>       Optional hidden file (contains _hidden_contents)
    #     <_archive_fn>      archive_url = file:///path/to/<_archive_fn>
    #
    def create_stage_archive(expected_file_list=[_include_readme]):
        tmpdir, test_stage_path = tmp_build_stage_dir
        test_stage_path.ensure(dir=True)

        # Create the archive directory and associated file
        archive_dir = tmpdir.join(_archive_base)
        archive = tmpdir.join(_archive_fn)
        archive_url = 'file://' + str(archive)
        archive_dir.ensure(dir=True)

        # Create the optional files as requested and make sure expanded
        # archive peers are included.
        tar_args = ['czf', str(_archive_fn), _archive_base]
        for _include in expected_file_list:
            if _include == _include_hidden:
                # The hidden file case stands in for the way Mac OS X tar files
                # represent HFS metadata.  Locate in the same directory as the
                # archive file.
                tar_args.append(_hidden_fn)
                fn, contents = (tmpdir.join(_hidden_fn), _hidden_contents)

            elif _include == _include_readme:
                # The usual README.txt file is contained in the archive dir.
                fn, contents = (archive_dir.join(_readme_fn), _readme_contents)

            elif _include == _include_extra:
                # The extra file stands in for exploding tar files so needs
                # to be in the same directory as the archive file.
                tar_args.append(_extra_fn)
                fn, contents = (tmpdir.join(_extra_fn), _extra_contents)
            else:
                break

            fn.write(contents)

        # Create the archive file
        with tmpdir.as_cwd():
            tar = spack.util.executable.which('tar', required=True)
            tar(*tar_args)

        Archive = collections.namedtuple(
            'Archive', ['url', 'tmpdir', 'stage_path', 'archive_dir']
        )
        return Archive(url=archive_url, tmpdir=tmpdir,
                       stage_path=test_stage_path, archive_dir=archive_dir)

    return create_stage_archive


@pytest.fixture
def mock_noexpand_resource(tmpdir):
    """Set up a non-expandable resource in the tmpdir prior to staging."""
    test_resource = tmpdir.join('resource-no-expand.sh')
    test_resource.write("an example resource")
    return str(test_resource)


@pytest.fixture
def mock_expand_resource(tmpdir):
    """Sets up an expandable resource in tmpdir prior to staging."""
    # Mock up an expandable resource:
    #
    # tmpdir/                    test_files_dir
    #     resource-expand/       resource source dir
    #         resource-file.txt  resource contents (contains 'test content')
    #     resource.tar.gz        archive of resource content
    #
    subdir = 'resource-expand'
    resource_dir = tmpdir.join(subdir)
    resource_dir.ensure(dir=True)

    archive_name = 'resource.tar.gz'
    archive = tmpdir.join(archive_name)
    archive_url = 'file://' + str(archive)

    filename = 'resource-file.txt'
    test_file = resource_dir.join(filename)
    test_file.write('test content\n')

    with tmpdir.as_cwd():
        tar = spack.util.executable.which('tar', required=True)
        tar('czf', str(archive_name), subdir)

    MockResource = collections.namedtuple(
        'MockResource', ['url', 'files'])

    return MockResource(archive_url, [filename])


@pytest.fixture
def composite_stage_with_expanding_resource(
        mock_stage_archive, mock_expand_resource):
    """Sets up a composite for expanding resources prior to staging."""
    composite_stage = StageComposite()
    archive = mock_stage_archive()
    root_stage = Stage(archive.url)
    composite_stage.append(root_stage)

    test_resource_fetcher = spack.fetch_strategy.from_kwargs(
        url=mock_expand_resource.url)
    # Specify that the resource files are to be placed in the 'resource-dir'
    # directory
    test_resource = Resource(
        'test_resource', test_resource_fetcher, '', 'resource-dir')
    resource_stage = ResourceStage(
        test_resource_fetcher, root_stage, test_resource)
    composite_stage.append(resource_stage)
    return composite_stage, root_stage, resource_stage, mock_expand_resource


@pytest.fixture
def failing_search_fn():
    """Returns a search function that fails! Always!"""
    def _mock():
        raise Exception("This should not have been called")
    return _mock


@pytest.fixture
def failing_fetch_strategy():
    """Returns a fetch strategy that fails."""
    class FailingFetchStrategy(spack.fetch_strategy.FetchStrategy):
        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                "<non-existent URL>",
                "This implementation of FetchStrategy always fails"
            )
    return FailingFetchStrategy()


@pytest.fixture
def search_fn():
    """Returns a search function that always succeeds."""
    class _Mock(object):
        performed_search = False

        def __call__(self):
            self.performed_search = True
            return []

    return _Mock()


def check_stage_dir_perms(prefix, path):
    """Check the stage directory perms to ensure match expectations."""
    # Ensure the path's subdirectories -- to `$user` -- have their parent's
    # perms while those from `$user` on are owned and restricted to the
    # user.
    status = os.stat(prefix)
    gid = status.st_gid
    uid = os.getuid()
    user = getpass.getuser()
    parts = path[len(prefix) + 1:].split(os.path.sep)
    have_user = False
    for part in parts:
        if part == user:
            have_user = True
        prefix = os.path.join(prefix, part)
        prefix_status = os.stat(prefix)
        if not have_user:
            assert gid == prefix_status.st_gid
            assert status.st_mode == prefix_status.st_mode
        else:
            assert uid == status.st_uid
            assert status.st_mode & stat.S_IRWXU == stat.S_IRWXU


@pytest.mark.usefixtures('mock_packages')
class TestStage(object):

    stage_name = 'spack-test-stage'

    def test_setup_and_destroy_name_with_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, archive)
        check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_name_without_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            check_setup(stage, self.stage_name, archive)
        check_destroy(stage, self.stage_name)

    def test_setup_and_destroy_no_name_with_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url) as stage:
            check_setup(stage, None, archive)
        check_destroy(stage, None)

    def test_noexpand_stage_file(
            self, mock_stage_archive, mock_noexpand_resource):
        """When creating a stage with a nonexpanding URL, the 'archive_file'
        property of the stage should refer to the path of that file.
        """
        test_noexpand_fetcher = spack.fetch_strategy.from_kwargs(
            url='file://' + mock_noexpand_resource, expand=False)
        with Stage(test_noexpand_fetcher) as stage:
            stage.fetch()
            stage.expand_archive()
            assert os.path.exists(stage.archive_file)

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_noexpand_resource(
            self, mock_stage_archive, mock_noexpand_resource):
        archive = mock_stage_archive()
        composite_stage = StageComposite()
        root_stage = Stage(archive.url)
        composite_stage.append(root_stage)

        resource_dst_name = 'resource-dst-name.sh'
        test_resource_fetcher = spack.fetch_strategy.from_kwargs(
            url='file://' + mock_noexpand_resource, expand=False)
        test_resource = Resource(
            'test_resource', test_resource_fetcher, resource_dst_name, None)
        resource_stage = ResourceStage(
            test_resource_fetcher, root_stage, test_resource)
        composite_stage.append(resource_stage)

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()
        assert composite_stage.expanded  # Archive is expanded

        assert os.path.exists(
            os.path.join(composite_stage.source_path, resource_dst_name))

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_expand_resource(
            self, composite_stage_with_expanding_resource):

        composite_stage, root_stage, resource_stage, mock_resource = (
            composite_stage_with_expanding_resource)

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()

        assert composite_stage.expanded  # Archive is expanded

        for fname in mock_resource.files:
            file_path = os.path.join(
                root_stage.source_path, 'resource-dir', fname)
            assert os.path.exists(file_path)

        # Perform a little cleanup
        shutil.rmtree(root_stage.path)

    @pytest.mark.disable_clean_stage_check
    def test_composite_stage_with_expand_resource_default_placement(
            self, composite_stage_with_expanding_resource):
        """For a resource which refers to a compressed archive which expands
        to a directory, check that by default the resource is placed in
        the source_path of the root stage with the name of the decompressed
        directory.
        """

        composite_stage, root_stage, resource_stage, mock_resource = (
            composite_stage_with_expanding_resource)

        resource_stage.resource.placement = None

        composite_stage.create()
        composite_stage.fetch()
        composite_stage.expand_archive()

        for fname in mock_resource.files:
            file_path = os.path.join(
                root_stage.source_path, 'resource-expand', fname)
            assert os.path.exists(file_path)

        # Perform a little cleanup
        shutil.rmtree(root_stage.path)

    def test_setup_and_destroy_no_name_without_tmp(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url) as stage:
            check_setup(stage, None, archive)
        check_destroy(stage, None)

    @pytest.mark.parametrize('debug', [False, True])
    def test_fetch(self, mock_stage_archive, debug):
        archive = mock_stage_archive()
        with spack.config.override('config:debug', debug):
            with Stage(archive.url, name=self.stage_name) as stage:
                stage.fetch()
                check_setup(stage, self.stage_name, archive)
                check_fetch(stage, self.stage_name)
            check_destroy(stage, self.stage_name)

    def test_no_search_if_default_succeeds(
            self, mock_stage_archive, failing_search_fn):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name,
                      search_fn=failing_search_fn)
        with stage:
            stage.fetch()
        check_destroy(stage, self.stage_name)

    def test_no_search_mirror_only(
            self, failing_fetch_strategy, failing_search_fn):
        stage = Stage(failing_fetch_strategy,
                      name=self.stage_name,
                      search_fn=failing_search_fn)
        with stage:
            try:
                stage.fetch(mirror_only=True)
            except spack.fetch_strategy.FetchError:
                pass
        check_destroy(stage, self.stage_name)

    def test_search_if_default_fails(self, failing_fetch_strategy, search_fn):
        stage = Stage(failing_fetch_strategy,
                      name=self.stage_name,
                      search_fn=search_fn)
        with stage:
            try:
                stage.fetch(mirror_only=False)
            except spack.fetch_strategy.FetchError:
                pass
        check_destroy(stage, self.stage_name)
        assert search_fn.performed_search

    def test_ensure_one_stage_entry(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            stage_path = get_stage_path(stage, self.stage_name)
            spack.fetch_strategy._ensure_one_stage_entry(stage_path)
        check_destroy(stage, self.stage_name)

    @pytest.mark.parametrize("expected_file_list", [
                             [],
                             [_include_readme],
                             [_include_extra, _include_readme],
                             [_include_hidden, _include_readme]])
    def test_expand_archive(self, expected_file_list, mock_stage_archive):
        archive = mock_stage_archive(expected_file_list)
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, archive)
            check_fetch(stage, self.stage_name)
            stage.expand_archive()
            check_expand_archive(stage, self.stage_name, expected_file_list)
        check_destroy(stage, self.stage_name)

    def test_expand_archive_extra_expand(self, mock_stage_archive):
        """Test expand with an extra expand after expand (i.e., no-op)."""
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            check_setup(stage, self.stage_name, archive)
            check_fetch(stage, self.stage_name)
            stage.expand_archive()
            stage.fetcher.expand()
            check_expand_archive(stage, self.stage_name, [_include_readme])
        check_destroy(stage, self.stage_name)

    def test_restage(self, mock_stage_archive):
        archive = mock_stage_archive()
        with Stage(archive.url, name=self.stage_name) as stage:
            stage.fetch()
            stage.expand_archive()

            with working_dir(stage.source_path):
                check_expand_archive(stage, self.stage_name, [_include_readme])

                # Try to make a file in the old archive dir
                with open('foobar', 'w') as file:
                    file.write("this file is to be destroyed.")

            assert 'foobar' in os.listdir(stage.source_path)

            # Make sure the file is not there after restage.
            stage.restage()
            check_fetch(stage, self.stage_name)
            assert 'foobar' not in os.listdir(stage.source_path)
        check_destroy(stage, self.stage_name)

    def test_no_keep_without_exceptions(self, mock_stage_archive):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=False)
        with stage:
            pass
        check_destroy(stage, self.stage_name)

    @pytest.mark.disable_clean_stage_check
    def test_keep_without_exceptions(self, mock_stage_archive):
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=True)
        with stage:
            pass
        path = get_stage_path(stage, self.stage_name)
        assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_no_keep_with_exceptions(self, mock_stage_archive):
        class ThisMustFailHere(Exception):
            pass

        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=False)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)

    @pytest.mark.disable_clean_stage_check
    def test_keep_exceptions(self, mock_stage_archive):
        class ThisMustFailHere(Exception):
            pass

        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name, keep=True)
        try:
            with stage:
                raise ThisMustFailHere()

        except ThisMustFailHere:
            path = get_stage_path(stage, self.stage_name)
            assert os.path.isdir(path)

    def test_source_path_available(self, mock_stage_archive):
        """Ensure source path available but does not exist on instantiation."""
        archive = mock_stage_archive()
        stage = Stage(archive.url, name=self.stage_name)

        source_path = stage.source_path
        assert source_path
        assert source_path.endswith(spack.stage._source_path_subdir)
        assert not os.path.exists(source_path)

    def test_first_accessible_path(self, tmpdir):
        """Test _first_accessible_path names."""
        spack_dir = tmpdir.join('spack-test-fap')
        name = str(spack_dir)
        files = [os.path.join(os.path.sep, 'no', 'such', 'path'), name]

        # Ensure the tmpdir path is returned since the user should have access
        path = spack.stage._first_accessible_path(files)
        assert path == name
        assert os.path.isdir(path)
        check_stage_dir_perms(str(tmpdir), path)

        # Ensure an existing path is returned
        spack_subdir = spack_dir.join('existing').ensure(dir=True)
        subdir = str(spack_subdir)
        path = spack.stage._first_accessible_path([subdir])
        assert path == subdir

        # Ensure a path with a `$user` node has the right permissions
        # for its subdirectories.
        user = getpass.getuser()
        user_dir = spack_dir.join(user, 'has', 'paths')
        user_path = str(user_dir)
        path = spack.stage._first_accessible_path([user_path])
        assert path == user_path
        check_stage_dir_perms(str(tmpdir), path)

        # Cleanup
        shutil.rmtree(str(name))

    def test_resolve_paths(self):
        """Test _resolve_paths."""

        assert spack.stage._resolve_paths([]) == []

        paths = [os.path.join(os.path.sep, 'a', 'b', 'c')]
        assert spack.stage._resolve_paths(paths) == paths

        tmp = '$tempdir'
        paths = [os.path.join(tmp, 'stage'), os.path.join(tmp, '$user')]
        can_paths = [canonicalize_path(paths[0]), canonicalize_path(tmp)]
        user = getpass.getuser()
        if user not in can_paths[1].split(os.path.sep):
            can_paths[1] = os.path.join(can_paths[1], user)
        assert spack.stage._resolve_paths(paths) == can_paths

    def test_get_stage_root_bad_path(self, clear_stage_root, bad_stage_path):
        """Ensure an invalid stage path root raises a StageError."""
        with pytest.raises(spack.stage.StageError,
                           match="No accessible stage paths in"):
            assert spack.stage.get_stage_root() is None

        # Make sure the cached stage path values are unchanged.
        assert spack.stage._stage_root is None

    def test_get_stage_root_non_user_path(self, clear_stage_root,
                                          non_user_path_for_stage):
        """Ensure a non-user stage root includes the username."""
        # The challenge here is whether the user has access to the standard
        # non-user path.  If not, the path should still appear in the error.
        try:
            path = spack.stage.get_stage_root()
            assert getpass.getuser() in path.split(os.path.sep)

            # Make sure the cached stage path values are changed appropriately.
            assert spack.stage._stage_root == path
        except OSError as e:
            expected = os.path.join(_non_user_root, getpass.getuser())
            assert expected in str(e)

            # Make sure the cached stage path values are unchanged.
            assert spack.stage._stage_root is None

    def test_get_stage_root_tmp(self, clear_stage_root, tmp_path_for_stage):
        """Ensure a temp path stage root is a suitable temp path."""
        assert spack.stage._stage_root is None

        tmpdir = tmp_path_for_stage
        path = spack.stage.get_stage_root()
        assert path == str(tmpdir)
        assert 'test_get_stage_root_tmp' in path

        # Make sure the cached stage path values are changed appropriately.
        assert spack.stage._stage_root == path

        # Add then purge a few directories
        dir1 = tmpdir.join('stage-1234567890abcdef1234567890abcdef')
        dir1.ensure(dir=True)
        dir2 = tmpdir.join('stage-abcdef12345678900987654321fedcba')
        dir2.ensure(dir=True)
        dir3 = tmpdir.join('stage-a1b2c3')
        dir3.ensure(dir=True)

        spack.stage.purge()
        assert not os.path.exists(str(dir1))
        assert not os.path.exists(str(dir2))
        assert os.path.exists(str(dir3))

        # Cleanup
        shutil.rmtree(str(dir3))

    def test_get_stage_root_in_spack(self, clear_stage_root,
                                     instance_path_for_stage):
        """Ensure an instance path stage root is a suitable path."""
        assert spack.stage._stage_root is None

        path = spack.stage.get_stage_root()
        assert 'spack' in path.split(os.path.sep)

        # Make sure the cached stage path values are changed appropriately.
        assert spack.stage._stage_root == path

    def test_stage_constructor_no_fetcher(self):
        """Ensure Stage constructor with no URL or fetch strategy fails."""
        with pytest.raises(ValueError):
            with Stage(None):
                pass

    def test_stage_constructor_with_path(self, tmpdir):
        """Ensure Stage constructor with a path uses it."""
        testpath = str(tmpdir)
        with Stage('file:///does-not-exist', path=testpath) as stage:
            assert stage.path == testpath

    def test_diystage_path_none(self):
        """Ensure DIYStage for path=None behaves as expected."""
        with pytest.raises(ValueError):
            DIYStage(None)

    def test_diystage_path_invalid(self):
        """Ensure DIYStage for an invalid path behaves as expected."""
        with pytest.raises(spack.stage.StagePathError):
            DIYStage('/path/does/not/exist')

    def test_diystage_path_valid(self, tmpdir):
        """Ensure DIYStage for a valid path behaves as expected."""
        path = str(tmpdir)
        stage = DIYStage(path)
        assert stage.path == path
        assert stage.source_path == path

        # Order doesn't really matter for DIYStage since they are
        # basically NOOPs; however, call each since they are part
        # of the normal stage usage and to ensure full test coverage.
        stage.create()  # Only sets the flag value
        assert stage.created

        stage.cache_local()  # Only outputs a message
        stage.fetch()  # Only outputs a message
        stage.check()  # Only outputs a message
        stage.expand_archive()  # Only outputs a message

        assert stage.expanded  # The path/source_path does exist

        with pytest.raises(spack.stage.RestageError):
            stage.restage()

        stage.destroy()  # A no-op
        assert stage.path == path  # Ensure can still access attributes
        assert os.path.exists(stage.source_path)  # Ensure path still exists

    def test_diystage_preserve_file(self, tmpdir):
        """Ensure DIYStage preserves an existing file."""
        # Write a file to the temporary directory
        fn = tmpdir.join(_readme_fn)
        fn.write(_readme_contents)

        # Instantiate the DIYStage and ensure the above file is unchanged.
        path = str(tmpdir)
        stage = DIYStage(path)
        assert os.path.isdir(path)
        assert os.path.isfile(str(fn))

        stage.create()  # Only sets the flag value

        readmefn = str(fn)
        assert os.path.isfile(readmefn)
        with open(readmefn) as _file:
            _file.read() == _readme_contents


@pytest.fixture
def tmp_build_stage_nondir(tmpdir):
    """Establish the temporary build_stage pointing to non-directory."""
    test_stage_path = tmpdir.join('stage', 'afile')
    test_stage_path.ensure(dir=False)

    # Set test_stage_path as the default directory to use for test stages.
    current = spack.config.get('config:build_stage')
    stage_dir = os.path.dirname(str(test_stage_path))
    spack.config.set('config', {'build_stage': [stage_dir]}, scope='user')

    yield test_stage_path

    spack.config.set('config', {'build_stage': current}, scope='user')


def test_stage_create_replace_path(tmp_build_stage_dir):
    """Ensure stage creation replaces a non-directory path."""
    _, test_stage_path = tmp_build_stage_dir
    test_stage_path.ensure(dir=True)

    nondir = test_stage_path.join('afile')
    nondir.ensure(dir=False)
    path = str(nondir)

    stage = Stage(path, name='')
    stage.create()  # Should ensure the path is converted to a dir

    assert os.path.isdir(stage.path)


def test_cannot_access():
    """Ensure can_access dies with the expected error."""
    with pytest.raises(SystemExit, matches='Insufficient permissions'):
        # It's far more portable to use a non-existent filename.
        spack.stage.ensure_access('/no/such/file')
