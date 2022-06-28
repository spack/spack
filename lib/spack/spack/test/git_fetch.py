# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import copy
import os
import re
import shutil
from textwrap import dedent

import pytest

from llnl.util.filesystem import mkdirp, touch, working_dir

import spack.config
import spack.repo
from spack.fetch_strategy import (
    ConfiguredGit,
    FailedGitFetch,
    FetcherConflict,
    GitFetchStageConfiguration,
    GitFetchStrategy,
    GitRef,
    InvalidGitFetchStageConfig,
    InvalidGitRef,
)
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which
from spack.version import ver

pytestmark = pytest.mark.skipif(
    not which('git'), reason='requires git to be installed')


_mock_transport_error = 'Mock HTTP transport error'


@pytest.fixture(params=[None, '1.8.5.2', '1.8.5.1',
                        '1.7.10', '1.7.1', '1.7.0'])
def git_version(request, monkeypatch):
    """Tests GitFetchStrategy behavior for different git versions.

    GitFetchStrategy tries to optimize using features of newer git
    versions, but needs to work with older git versions.  To ensure code
    paths for old versions still work, we fake it out here and make it
    use the backward-compatibility code paths with newer git versions.
    """
    git = which('git', required=True)
    real_git_version = spack.fetch_strategy.ConfiguredGit.from_executable(git).version

    if request.param is None:
        # Don't patch; run with the real git_version method.
        yield real_git_version
    else:
        test_git_version = ver(request.param)
        if test_git_version > real_git_version:
            pytest.skip("Can't test clone logic for newer version of git.")

        # Patch the fetch strategy to think it's using a lower git version.
        # we use this to test what we'd need to do with older git versions
        # using a newer git installation.
        def get_test_git_version(_cls, _git):
            return test_git_version
        monkeypatch.setattr(ConfiguredGit, '_get_git_version',
                            # Need to explicitly bind the function to the class for py2.
                            get_test_git_version.__get__(ConfiguredGit))
        yield test_git_version


@pytest.fixture
def mock_bad_git(monkeypatch):
    """
    Test GitFetchStrategy behavior with a bad git command for git >= 1.7.1
    to trigger a SpackError.
    """
    def bad_git(*args, **kwargs):
        """Raise a SpackError with the transport message."""
        raise spack.error.SpackError(_mock_transport_error)

    # Patch the fetch strategy to think it's using a git version that
    # will error out when git is called.
    bad_git = ConfiguredGit(bad_git, ver('1.7.1'))
    monkeypatch.setattr(ConfiguredGit, 'from_executable', lambda _: bad_git)
    yield


def test_bad_git(tmpdir, mock_bad_git):
    """Trigger a SpackError when attempt a fetch with a bad git."""
    testpath = str(tmpdir)

    with pytest.raises(spack.error.SpackError):
        fetcher = GitFetchStrategy(git='file:///not-a-real-git-repo')
        with Stage(fetcher, path=testpath):
            fetcher.fetch()


@pytest.mark.parametrize("type_of_test",
                         ['default', 'branch', 'tag', 'commit'])
@pytest.mark.parametrize("secure", [True, False])
def test_git_fetch(type_of_test,
                   secure,
                   mock_git_repository,
                   config,
                   mutable_mock_repo,
                   git_version,
                   monkeypatch,
                   patch_from_version_directive_for_git_ref):
    """Performs multiple operations in series for a given refspec.

    1. Fetch the repo using a git fetch strategy constructed with
       supplied args (they depend on type_of_test).
    2. Check if the test_file is in the checked out repository.
    3. Assert that the repository is at the revision supplied.
    4. Add and remove some files, then reset the repo, and
       ensure it's all there again.
    """
    # Retrieve the right test parameters
    if type_of_test.startswith('tag-'):
        t = mock_git_repository.checks['tag']
    elif type_of_test.startswith('branch-'):
        t = mock_git_repository.checks['branch']
    else:
        t = mock_git_repository.checks[type_of_test]
    h = mock_git_repository.hash

    pkg_class = spack.repo.path.get_pkg_class('git-test')
    # This would fail using the default-no-per-version-git check but that
    # isn't included in this test
    monkeypatch.delattr(pkg_class, 'git')

    if type_of_test == 'default':
        git_ref = GitRef.Branch(t.revision)
    elif type_of_test == 'branch':
        git_ref = GitRef.Branch(t.revision)
    elif type_of_test == 'tag':
        git_ref = GitRef.Tag(t.revision)
    elif type_of_test == 'commit':
        git_ref = GitRef.Commit(t.revision)
    elif type_of_test == 'tag-with-commit-matching':
        git_ref = GitRef.Tag(t.revision,
                             commit=mock_git_repository.checks['tag'].hash)
    elif type_of_test == 'tag-with-commit-non-matching':
        git_ref = GitRef.Tag(t.revision, commit='asdf')
    elif type_of_test == 'branch-with-commit-matching':
        git_ref = GitRef.Branch(t.revision,
                                commit=mock_git_repository.checks['branch'].hash)
    else:
        assert type_of_test == 'branch-with-commit-non-matching', type_of_test
        git_ref = GitRef.Branch(t.revision, commit='asdf')
    patch_from_version_directive_for_git_ref(git_ref)

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    monkeypatch.setitem(pkg.versions, ver('git'), t.args)

    # Enter the stage directory and check some properties
    with pkg.stage:
        with spack.config.override('config:verify_ssl', secure):
            # Verify that if either 'tag' and 'branch' are provided along with 'commit',
            # that the value of 'commit' is checked against the hash that the tag or
            # branch resolves to.
            commit_hash = None
            if type_of_test == 'tag-with-commit-non-matching':
                commit_hash = mock_git_repository.checks['tag'].hash
            elif type_of_test == 'branch-with-commit-non-matching':
                commit_hash = mock_git_repository.checks['branch'].hash

            if commit_hash is not None:
                exc_msg = dedent("""\
                The git checkout produced a commit {}, which did not match the commit
                hash prefix {}!
                """.format(commit_hash, git_ref.should_validate_matches_hash()))
                with pytest.raises(InvalidGitRef, match=exc_msg):
                    pkg.do_stage()
                return

            pkg.do_stage()

        with working_dir(pkg.stage.source_path):
            assert h('HEAD') == h(t.revision)

            file_path = os.path.join(pkg.stage.source_path, t.file)
            assert os.path.isdir(pkg.stage.source_path)
            assert os.path.isfile(file_path)

            os.unlink(file_path)
            assert not os.path.isfile(file_path)

            untracked_file = 'foobarbaz'
            touch(untracked_file)
            assert os.path.isfile(untracked_file)

        # A restage will delete the stage directory, so we need to get out of the above
        # working_dir() scope and then re-acquire it at the same path.
        with spack.config.override('config:verify_ssl', secure):
            pkg.do_restage()

        with working_dir(pkg.stage.source_path):
            assert not os.path.isfile(untracked_file)

            assert os.path.isdir(pkg.stage.source_path)
            assert os.path.isfile(file_path)

            assert h('HEAD') == h(t.revision)


@pytest.mark.disable_clean_stage_check
def test_fetch_pkg_attr_submodule_init(
        mock_git_repository,
        config,
        mutable_mock_repo,
        monkeypatch,
        mock_stage):
    """In this case the version() args do not contain a 'git' URL, so
    the fetcher must be assembled using the Package-level 'git' attribute.
    This test ensures that the submodules are properly initialized and the
    expected branch file is present.
    """

    t = mock_git_repository.checks['default-no-per-version-git']
    pkg_class = spack.repo.path.get_pkg_class('git-test')
    # For this test, the version args don't specify 'git' (which is
    # the majority of version specifications)
    monkeypatch.setattr(pkg_class, 'git', mock_git_repository.url)

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    monkeypatch.setitem(pkg.versions, ver('git'), t.args)

    spec.package.do_stage()

    collected_fnames = set()
    for root, dirs, files in os.walk(spec.package.stage.source_path):
        collected_fnames.update(files)
    # The submodules generate files with the prefix "r0_file_"
    assert set(['r0_file_0', 'r0_file_1', t.file]) < collected_fnames


@pytest.mark.skipif(str(spack.platforms.host()) == 'windows',
                    reason=('Git fails to clone because the src/dst paths'
                            ' are too long: the name of the staging directory'
                            ' for ad-hoc Git commit versions is longer than'
                            ' other staged sources'))
@pytest.mark.disable_clean_stage_check
def test_adhoc_version_submodules(
        mock_git_repository,
        config,
        mutable_mock_repo,
        monkeypatch,
        mock_stage,
        patch_from_version_directive_for_git_ref,
):

    t = mock_git_repository.checks['tag']
    # Construct the package under test
    pkg_class = spack.repo.path.get_pkg_class('git-test')
    monkeypatch.setitem(pkg_class.versions, ver('git'), t.args)
    monkeypatch.setattr(pkg_class, 'git', 'file://%s' % mock_git_repository.path,
                        raising=False)

    patch_from_version_directive_for_git_ref(
        GitRef.Commit(mock_git_repository.unversioned_commit),
    )
    spec = Spec('git-test@{0}'.format(mock_git_repository.unversioned_commit))
    spec.concretize()
    spec.package.do_stage()
    collected_fnames = set()
    for root, dirs, files in os.walk(spec.package.stage.source_path):
        collected_fnames.update(files)
    # The submodules generate files with the prefix "r0_file_"
    assert set(['r0_file_0', 'r0_file_1']) < collected_fnames


@pytest.mark.parametrize("type_of_test", ['branch', 'commit'])
def test_debug_fetch(
        mock_packages, type_of_test, mock_git_repository, config, monkeypatch
):
    """Fetch the repo with debug enabled."""
    # Retrieve the right test parameters
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    monkeypatch.setitem(pkg.versions, ver('git'), t.args)

    # Fetch then ensure source path exists
    with pkg.stage:
        with spack.config.override('config:debug', True):
            pkg.do_fetch()
            assert os.path.isdir(pkg.stage.source_path)


def test_git_extra_fetch(tmpdir):
    """Ensure a fetch after 'expanding' is effectively a no-op."""
    testpath = str(tmpdir)

    fetcher = GitFetchStrategy(
        git='file:///not-a-real-git-repo',
        branch='asdf',
    )
    with Stage(fetcher, path=testpath) as stage:
        mkdirp(stage.source_path)
        with pytest.raises(
            FailedGitFetch,
            match=re.escape(
                "'/not-a-real-git-repo' does not appear to be a git repository",
            ),
        ):
            fetcher.fetch()   # Use fetcher to fetch for code coverage
        shutil.rmtree(stage.source_path)


def test_needs_stage():
    """Trigger a NoStageError when attempt a fetch without a stage."""
    with pytest.raises(spack.fetch_strategy.NoStageError,
                       match=r"set_stage.*before calling fetch"):
        fetcher = GitFetchStrategy(git='file:///not-a-real-git-repo', branch='master')
        fetcher.fetch()


@pytest.mark.parametrize("get_full_repo", [True, False])
def test_get_full_repo(get_full_repo, git_version, mock_git_repository,
                       config, mutable_mock_repo, monkeypatch):
    """Ensure that we can clone a full repository."""

    if git_version < ver('1.7.1'):
        pytest.skip('Not testing get_full_repo for older git {0}'.
                    format(git_version))

    secure = True
    type_of_test = 'tag-branch'

    t = mock_git_repository.checks[type_of_test]

    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    args = copy.copy(t.args)
    args['get_full_repo'] = get_full_repo
    monkeypatch.setitem(pkg.versions, ver('git'), args)

    with pkg.stage:
        with spack.config.override('config:verify_ssl', secure):
            pkg.do_stage()

            with working_dir(pkg.stage.source_path):
                # `git branch` will occasionally print out a '+' at the start of
                # a branch, which isn't relevant for us and appears to change across git
                # versions.
                branches\
                    = [re.sub(r'^\+', ' ', branch_line)
                       for branch_line in
                       mock_git_repository.git_exe('branch', '-a', output=str)
                       .splitlines()]
                git_log_lines\
                    = mock_git_repository.\
                    git_exe('log', '--graph',
                            '--pretty=format:%h -%d %s (%ci) <%an>',
                            '--abbrev-commit',
                            output=str).splitlines()

                commits = [re.sub(r'\* ([a-z0-9]+) .*$', r'\1', log_line)
                           for log_line in git_log_lines]

        if get_full_repo:
            assert branches[0] == '* (no branch)'
            assert branches[1].startswith('  refs/heads/spack-internal-'), branches
            assert branches[2:] == ['  tag-branch']
            assert len(commits) == 3
        else:
            assert branches[0] == '* (no branch)'
            assert branches[1].startswith('  refs/heads/spack-internal-'), branches
            assert branches[2:] == ['  tag-branch']
            assert len(commits) == 1


@pytest.mark.disable_clean_stage_check
@pytest.mark.parametrize("submodules", [True, False])
def test_gitsubmodule(submodules, mock_git_repository, config,
                      mutable_mock_repo, monkeypatch):
    """
    Test GitFetchStrategy behavior with submodules. This package
    has a `submodules` property which is always True: when a specific
    version also indicates to include submodules, this should not
    interfere; if the specific version explicitly requests that
    submodules *not* be initialized, this should override the
    Package-level request.
    """
    type_of_test = 'tag-branch'
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    args = copy.copy(t.args)
    args['submodules'] = submodules
    monkeypatch.setitem(pkg.versions, ver('git'), args)
    pkg.do_stage()
    with working_dir(pkg.stage.source_path):
        for submodule_count in range(2):
            file_path = os.path.join(pkg.stage.source_path,
                                     'third_party/submodule{0}/r0_file_{0}'
                                     .format(submodule_count))
            if submodules:
                assert os.path.isfile(file_path)
            else:
                assert not os.path.isfile(file_path)


@pytest.mark.disable_clean_stage_check
def test_gitsubmodules_callable(
        mock_git_repository, config, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior with submodules selected after concretization
    """
    def submodules_callback(package):
        name = 'third_party/submodule0'
        return [name]

    type_of_test = 'tag-branch'
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    args = copy.copy(t.args)
    args['submodules'] = submodules_callback
    monkeypatch.setitem(pkg.versions, ver('git'), args)
    pkg.do_stage()
    with working_dir(pkg.stage.source_path):
        file_path = os.path.join(pkg.stage.source_path,
                                 'third_party/submodule0/r0_file_0')
        assert os.path.isfile(file_path)
        file_path = os.path.join(pkg.stage.source_path,
                                 'third_party/submodule1/r0_file_1')
        assert not os.path.isfile(file_path)


@pytest.mark.disable_clean_stage_check
def test_gitsubmodules_delete(
        mock_git_repository, config, mutable_mock_repo, monkeypatch
):
    """
    Test GitFetchStrategy behavior with submodules_delete
    """
    type_of_test = 'tag-branch'
    t = mock_git_repository.checks[type_of_test]

    # Construct the package under test
    spec = Spec('git-test')
    spec.concretize()
    pkg = spack.repo.get(spec)
    args = copy.copy(t.args)
    args['submodules'] = True
    args['submodules_delete'] = ['third_party/submodule0',
                                 'third_party/submodule1']
    monkeypatch.setitem(pkg.versions, ver('git'), args)
    pkg.do_stage()
    with working_dir(pkg.stage.source_path):
        file_path = os.path.join(pkg.stage.source_path,
                                 'third_party/submodule0')
        assert not os.path.isdir(file_path)
        file_path = os.path.join(pkg.stage.source_path,
                                 'third_party/submodule1')
        assert not os.path.isdir(file_path)


class TestGitRef(object):
    """Trigger an error when a GitRef is constructed incorrectly."""

    class NewGitRef(GitRef):
        ref_type = 'asdf'

        def should_validate_matches_hash(self):
            return None

    def test_parsing_invalid_type(self):
        """GitRef subtypes need to be registered in GitRef._known_types!"""
        with pytest.raises(TypeError, match="can only have the types.*given 'asdf'"):
            self.NewGitRef('<anything>')

    @pytest.mark.parametrize('ref_type', GitRef.known_types)
    def test_parsing_non_string_value(self, ref_type):
        with pytest.raises(InvalidGitRef, match="was not a string: 2"):
            getattr(GitRef, ref_type)(2)

    @pytest.mark.parametrize('allowable_hash_length', [7, 10, 32, 40])
    def test_allowable_hash_length(self, allowable_hash_length):
        allowable_hash = 'a' * allowable_hash_length
        _ = GitRef.Commit(allowable_hash)

    @pytest.mark.parametrize('incorrect_hash_length', [5, 42])
    def test_invalid_hash_length(self, incorrect_hash_length):
        bad_hash = 'a' * incorrect_hash_length
        err_rx = ("7-40 character hexadecimal string, but received {0!r} instead"
                  .format(bad_hash))
        with pytest.raises(InvalidGitRef, match=err_rx):
            GitRef.Commit(bad_hash)

    @pytest.mark.parametrize('bad_hash', ['atwwes73'])
    def test_invalid_hash_string_content(self, bad_hash):
        err_rx = ("7-40 character hexadecimal string, but received {0!r} instead"
                  .format(bad_hash))
        with pytest.raises(InvalidGitRef, match=err_rx):
            GitRef.Commit(bad_hash)

    def test_parsing_empty_version_directive(self):
        err_rx = "Given:\ncommit=None(.|\n)+tag=None(.|\n)+branch=None"
        with pytest.raises(InvalidGitRef, match=err_rx):
            GitRef.from_version_directive(dict())

    def test_parsing_version_name_only(self):
        version_name_only = GitRef.from_version_directive(dict(version_name='asdf'))
        assert version_name_only.ref_type == 'Branch'
        assert version_name_only.refspec() == 'refs/heads/asdf'

    _VALID_INDIVIDUAL_ARGS = dict(tag='asdf', branch='fdsa', commit='a' * 7)

    @pytest.mark.parametrize('ref_type,ref_name', _VALID_INDIVIDUAL_ARGS.items())
    def test_successfully_parsing_version_directive(self, ref_type, ref_name):
        ref = GitRef.from_version_directive({ref_type: ref_name})
        assert ref.ref_type.lower() == ref_type.lower()
        assert ref.refspec().endswith(ref_name), ref

    def test_mutually_exclusive_kwargs_error(self):
        mutually_exclusive_kwargs = dict(
            tag='asdf',
            branch='fdsa',
        )
        with pytest.raises(InvalidGitRef,
                           match=dedent("""\
                           tag=asdf
                           branch=fdsa
                           """)):
            GitRef.from_version_directive(mutually_exclusive_kwargs)


class TestGitFetchStageConfiguration(object):
    """Trigger an error when a GitFetchStageConfiguration is constructed incorrectly."""

    @pytest.mark.parametrize('kwargs', [
        {},
        dict(submodules=True,
             submodules_delete=['something'],
             get_full_repo=True),
        dict(submodules=False,
             submodules_delete=None,
             get_full_repo=False),
    ])
    def test_successful_parsing_of_version_directive(self, kwargs):
        _ = GitFetchStageConfiguration.from_version_directive(kwargs)

    @pytest.mark.parametrize('kwargs', [
        dict(submodules='True'),
        dict(submodules='False'),
        dict(submodules_delete='asdf'),
        dict(get_full_repo='True'),
        dict(get_full_repo='False'),
    ])
    def test_failed_parsing_of_version_directive(self, kwargs):
        with pytest.raises(InvalidGitFetchStageConfig):
            GitFetchStageConfiguration.from_version_directive(kwargs)


class TestGitFetchStrategy(object):
    """Trigger a FetcherConflict when a parsed version() is ambiguous or malformed."""

    @pytest.mark.parametrize('kwargs', [
        dict(git='file:///not-a-real-git-repo', branch='master',
             submodules=True, submodules_delete=['something'], get_full_repo=True),
        dict(git='file:///not-a-real-git-repo', branch='master',
             submodules=False, submodules_delete=None, get_full_repo=False),
        dict(git='file:///not-a-real-git-repo', version_name='master',
             submodules=False, submodules_delete=None, get_full_repo=False),
        dict(git='file:///not-a-real-git-repo', commit='asdf', tag='fdsa'),
    ])
    def test_successful_parsing(self, kwargs):
        _ = GitFetchStrategy(**kwargs)

    @pytest.mark.parametrize('kwargs', [
        dict(git='file:///not-a-real-git-repo'),
        dict(git='file:///not-a-real-git-repo', tag='asdf', branch='fdsa'),
    ])
    def test_raises_on_invalid_ref(self, kwargs):
        """Raises for invalid version() specifications."""
        with pytest.raises(FetcherConflict,
                           match=r"Failed to identify an unambiguous refspec"):
            GitFetchStrategy(**kwargs)

    @pytest.mark.parametrize('kwargs,err_rx', [
        (dict(git='file:///not-a-real-git-repo', branch='master', submodules='True'),
         "submodules=.*must be a bool"),
        (dict(git='file:///not-a-real-git-repo', branch='master',
              submodules_delete='something'),
         "submodules_delete=.*must be a list of str"),
        (dict(git='file:///not-a-real-git-repo', branch='master', get_full_repo='True'),
         "get_full_repo=.*must be a bool"),
    ])
    def test_raises_on_invalid_stage_config(self, kwargs, err_rx):
        """Raises for invalid info to prepare the checkout for the spack stage."""
        with pytest.raises(FetcherConflict, match=err_rx):
            GitFetchStrategy(**kwargs)
