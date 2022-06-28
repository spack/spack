# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Fetch strategies are used to download source code into a staging area
in order to build it.  They need to define the following methods:

    * fetch()
        This should attempt to download/check out source from somewhere.
    * check()
        Apply a checksum to the downloaded source code, e.g. for an archive.
        May not do anything if the fetch method was safe to begin with.
    * expand()
        Expand (e.g., an archive) downloaded file to source, with the
        standard stage source path as the destination directory.
    * reset()
        Restore original state of downloaded code.  Used by clean commands.
        This may just remove the expanded source and re-expand an archive,
        or it may run something like git reset --hard.
    * archive()
        Archive a source directory, e.g. for creating a mirror.
"""
import abc
import copy
import functools
import os
import os.path
import re
import shutil
import sys
import uuid
from textwrap import dedent
from typing import (  # novm
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import six
import six.moves.urllib.parse as urllib_parse

import llnl.util
import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty
from llnl.util.filesystem import (
    get_single_file,
    mkdirp,
    temp_cwd,
    temp_rename,
    working_dir,
)
from llnl.util.symlink import symlink

import spack.config
import spack.error
import spack.util.crypto as crypto
import spack.util.pattern as pattern
import spack.util.url as url_util
import spack.util.web
import spack.version
from spack.util.compression import decompressor_for, extension
from spack.util.executable import CommandNotFoundError, Executable, ProcessError, which
from spack.util.string import comma_and, quote

if TYPE_CHECKING:
    from spack.package_base import PackageBase

#: List of all fetch strategies, created by FetchStrategy metaclass.
all_strategies = []
is_windows = sys.platform == 'win32'

CONTENT_TYPE_MISMATCH_WARNING_TEMPLATE = (
    "The contents of {subject} look like {content_type}.  Either the URL"
    " you are trying to use does not exist or you have an internet gateway"
    " issue.  You can remove the bad archive using 'spack clean"
    " <package>', then try again using the correct URL.")


def warn_content_type_mismatch(subject, content_type='HTML'):
    tty.warn(CONTENT_TYPE_MISMATCH_WARNING_TEMPLATE.format(
        subject=subject, content_type=content_type))


def _needs_stage(fun):
    """Many methods on fetch strategies require a stage to be set
       using set_stage().  This decorator adds a check for self.stage."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        if not self.stage:
            raise NoStageError(fun)
        return fun(self, *args, **kwargs)

    return wrapper


def _ensure_one_stage_entry(stage_path):
    """Ensure there is only one stage entry in the stage path."""
    stage_entries = os.listdir(stage_path)
    assert len(stage_entries) == 1
    return os.path.join(stage_path, stage_entries[0])


def fetcher(cls):
    """Decorator used to register fetch strategies."""
    all_strategies.append(cls)
    return cls


class FetchStrategy(object):
    """Superclass of all fetch strategies."""
    #: The URL attribute must be specified either at the package class
    #: level, or as a keyword argument to ``version()``.  It is used to
    #: distinguish fetchers for different versions in the package DSL.
    url_attr = None  # type: Optional[str]

    #: Optional attributes can be used to distinguish fetchers when :
    #: classes have multiple ``url_attrs`` at the top-level.
    # optional attributes in version() args.
    optional_attrs = []  # type: List[str]

    def __init__(self, **kwargs):
        # The stage is initialized late, so that fetch strategies can be
        # constructed at package construction time.  This is where things
        # will be fetched.
        self.stage = None
        # Enable or disable caching for this strategy based on
        # 'no_cache' option from version directive.
        self.cache_enabled = not kwargs.pop('no_cache', False)

        self.package = None

    def set_package(self, package):
        self.package = package

    # Subclasses need to implement these methods
    def fetch(self):
        """Fetch source code archive or repo.

        Returns:
            bool: True on success, False on failure.
        """

    def check(self):
        """Checksum the archive fetched by this FetchStrategy."""

    def expand(self):
        """Expand the downloaded archive into the stage source path."""

    def reset(self):
        """Revert to freshly downloaded state.

        For archive files, this may just re-expand the archive.
        """

    def archive(self, destination):
        """Create an archive of the downloaded data for a mirror.

        For downloaded files, this should preserve the checksum of the
        original file. For repositories, it should just create an
        expandable tarball out of the downloaded repository.
        """

    @property
    def cachable(self):
        """Whether fetcher is capable of caching the resource it retrieves.

        This generally is determined by whether the resource is
        identifiably associated with a specific package version.

        Returns:
            bool: True if can cache, False otherwise.
        """

    def source_id(self):
        """A unique ID for the source.

        It is intended that a human could easily generate this themselves using
        the information available to them in the Spack package.

        The returned value is added to the content which determines the full
        hash for a package using `str()`.
        """
        raise NotImplementedError

    def mirror_id(self):
        """This is a unique ID for a source that is intended to help identify
        reuse of resources across packages.

        It is unique like source-id, but it does not include the package name
        and is not necessarily easy for a human to create themselves.
        """
        raise NotImplementedError

    def __str__(self):  # Should be human readable URL.
        return "FetchStrategy.__str___"

    @classmethod
    def matches(cls, args):
        """Predicate that matches fetch strategies to arguments of
        the version directive.

        Args:
            args: arguments of the version directive
        """
        return cls.url_attr in args


@fetcher
class BundleFetchStrategy(FetchStrategy):
    """
    Fetch strategy associated with bundle, or no-code, packages.

    Having a basic fetch strategy is a requirement for executing post-install
    hooks.  Consequently, this class provides the API but does little more
    than log messages.

    TODO: Remove this class by refactoring resource handling and the link
    between composite stages and composite fetch strategies (see #11981).
    """
    #: There is no associated URL keyword in ``version()`` for no-code
    #: packages but this property is required for some strategy-related
    #: functions (e.g., check_pkg_attributes).
    url_attr = ''

    def fetch(self):
        """Simply report success -- there is no code to fetch."""
        return True

    @property
    def cachable(self):
        """Report False as there is no code to cache."""
        return False

    def source_id(self):
        """BundlePackages don't have a source id."""
        return ''

    def mirror_id(self):
        """BundlePackages don't have a mirror id."""


class FetchStrategyComposite(pattern.Composite):
    """Composite for a FetchStrategy object.
    """
    matches = FetchStrategy.matches

    def __init__(self):
        super(FetchStrategyComposite, self).__init__([
            'fetch', 'check', 'expand', 'reset', 'archive', 'cachable',
            'mirror_id'
        ])

    def source_id(self):
        component_ids = tuple(i.source_id() for i in self)
        if all(component_ids):
            return component_ids

    def set_package(self, package):
        for item in self:
            item.package = package


@fetcher
class URLFetchStrategy(FetchStrategy):
    """URLFetchStrategy pulls source code from a URL for an archive, check the
    archive against a checksum, and decompresses the archive.

    The destination for the resulting file(s) is the standard stage path.
    """
    url_attr = 'url'

    # these are checksum types. The generic 'checksum' is deprecated for
    # specific hash names, but we need it for backward compatibility
    optional_attrs = list(crypto.hashes.keys()) + ['checksum']

    def __init__(self, url=None, checksum=None, **kwargs):
        super(URLFetchStrategy, self).__init__(**kwargs)

        # Prefer values in kwargs to the positionals.
        self.url = kwargs.get('url', url)
        self.mirrors = kwargs.get('mirrors', [])

        # digest can be set as the first argument, or from an explicit
        # kwarg by the hash name.
        self.digest = kwargs.get('checksum', checksum)
        for h in self.optional_attrs:
            if h in kwargs:
                self.digest = kwargs[h]

        self.expand_archive = kwargs.get('expand', True)
        self.extra_options = kwargs.get('fetch_options', {})
        self._curl = None

        self.extension = kwargs.get('extension', None)

        if not self.url:
            raise ValueError("URLFetchStrategy requires a url for fetching.")

    @property
    def curl(self):
        if not self._curl:
            try:
                self._curl = which('curl', required=True)
            except CommandNotFoundError as exc:
                tty.error(str(exc))
        return self._curl

    def source_id(self):
        return self.digest

    def mirror_id(self):
        if not self.digest:
            return None
        # The filename is the digest. A directory is also created based on
        # truncating the digest to avoid creating a directory with too many
        # entries
        return os.path.sep.join(
            ['archive', self.digest[:2], self.digest])

    @property
    def candidate_urls(self):
        urls = []

        for url in [self.url] + (self.mirrors or []):
            # This must be skipped on Windows due to URL encoding
            # of ':' characters on filepaths on Windows
            if sys.platform != "win32" and url.startswith('file://'):
                path = urllib_parse.quote(url[len('file://'):])
                url = 'file://' + path
            urls.append(url)

        return urls

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.debug('Already downloaded {0}'.format(self.archive_file))
            return

        url = None
        errors = []
        for url in self.candidate_urls:
            if not self._existing_url(url):
                continue

            try:
                partial_file, save_file = self._fetch_from_url(url)
                if save_file and (partial_file is not None):
                    llnl.util.filesystem.rename(partial_file, save_file)
                break
            except FailedDownloadError as e:
                errors.append(str(e))

        for msg in errors:
            tty.debug(msg)

        if not self.archive_file:
            raise FailedDownloadError(url)

    def _existing_url(self, url):
        tty.debug('Checking existence of {0}'.format(url))

        if spack.config.get('config:url_fetch_method') == 'curl':
            curl = self.curl
            # Telling curl to fetch the first byte (-r 0-0) is supposed to be
            # portable.
            curl_args = ['--stderr', '-', '-s', '-f', '-r', '0-0', url]
            if not spack.config.get('config:verify_ssl'):
                curl_args.append('-k')
            _ = curl(*curl_args, fail_on_error=False, output=os.devnull)
            return curl.returncode == 0
        else:
            # Telling urllib to check if url is accessible
            try:
                url, headers, response = spack.util.web.read_from_url(url)
            except spack.util.web.SpackWebError as werr:
                msg = "Urllib fetch failed to verify url\
                      {0}\n with error {1}".format(url, werr)
                raise FailedDownloadError(url, msg)
            return (response.getcode() is None or response.getcode() == 200)

    def _fetch_from_url(self, url):
        if spack.config.get('config:url_fetch_method') == 'curl':
            return self._fetch_curl(url)
        else:
            return self._fetch_urllib(url)

    def _check_headers(self, headers):
        # Check if we somehow got an HTML file rather than the archive we
        # asked for.  We only look at the last content type, to handle
        # redirects properly.
        content_types = re.findall(r'Content-Type:[^\r\n]+', headers,
                                   flags=re.IGNORECASE)
        if content_types and 'text/html' in content_types[-1]:
            warn_content_type_mismatch(self.archive_file or "the archive")

    @_needs_stage
    def _fetch_urllib(self, url):
        save_file = None
        if self.stage.save_filename:
            save_file = self.stage.save_filename
        tty.msg('Fetching {0}'.format(url))

        # Run urllib but grab the mime type from the http headers
        try:
            url, headers, response = spack.util.web.read_from_url(url)
        except spack.util.web.SpackWebError as e:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)
            if save_file and os.path.exists(save_file):
                os.remove(save_file)
            msg = 'urllib failed to fetch with error {0}'.format(e)
            raise FailedDownloadError(url, msg)

        with open(save_file, 'wb') as _open_file:
            shutil.copyfileobj(response, _open_file)

        self._check_headers(str(headers))
        return None, save_file

    @_needs_stage
    def _fetch_curl(self, url):
        save_file = None
        partial_file = None
        if self.stage.save_filename:
            save_file = self.stage.save_filename
            partial_file = self.stage.save_filename + '.part'
        tty.msg('Fetching {0}'.format(url))
        if partial_file:
            save_args = ['-C',
                         '-',  # continue partial downloads
                         '-o',
                         partial_file]  # use a .part file
        else:
            save_args = ['-O']

        curl_args = save_args + [
            '-f',  # fail on >400 errors
            '-D',
            '-',  # print out HTML headers
            '-L',  # resolve 3xx redirects
            url,
        ]

        if not spack.config.get('config:verify_ssl'):
            curl_args.append('-k')

        if sys.stdout.isatty() and tty.msg_enabled():
            curl_args.append('-#')  # status bar when using a tty
        else:
            curl_args.append('-sS')  # show errors if fail

        connect_timeout = spack.config.get('config:connect_timeout', 10)

        if self.extra_options:
            cookie = self.extra_options.get('cookie')
            if cookie:
                curl_args.append('-j')  # junk cookies
                curl_args.append('-b')  # specify cookie
                curl_args.append(cookie)

            timeout = self.extra_options.get('timeout')
            if timeout:
                connect_timeout = max(connect_timeout, int(timeout))

        if connect_timeout > 0:
            # Timeout if can't establish a connection after n sec.
            curl_args.extend(['--connect-timeout', str(connect_timeout)])

        # Run curl but grab the mime type from the http headers
        curl = self.curl
        with working_dir(self.stage.path):
            headers = curl(*curl_args, output=str, fail_on_error=False)

        if curl.returncode != 0:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)

            if partial_file and os.path.exists(partial_file):
                os.remove(partial_file)

            if curl.returncode == 22:
                # This is a 404.  Curl will print the error.
                raise FailedDownloadError(
                    url, "URL %s was not found!" % url)

            elif curl.returncode == 60:
                # This is a certificate error.  Suggest spack -k
                raise FailedDownloadError(
                    url,
                    "Curl was unable to fetch due to invalid certificate. "
                    "This is either an attack, or your cluster's SSL "
                    "configuration is bad.  If you believe your SSL "
                    "configuration is bad, you can try running spack -k, "
                    "which will not check SSL certificates."
                    "Use this at your own risk.")

            else:
                # This is some other curl error.  Curl will print the
                # error, but print a spack message too
                raise FailedDownloadError(
                    url,
                    "Curl failed with error %d" % curl.returncode)

        self._check_headers(headers)
        return partial_file, save_file

    @property  # type: ignore # decorated properties unsupported in mypy
    @_needs_stage
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        return self.stage.archive_file

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.digest)

    @_needs_stage
    def expand(self):
        if not self.expand_archive:
            tty.debug('Staging unexpanded archive {0} in {1}'
                      .format(self.archive_file, self.stage.source_path))
            if not self.stage.expanded:
                mkdirp(self.stage.source_path)
            dest = os.path.join(self.stage.source_path,
                                os.path.basename(self.archive_file))
            shutil.move(self.archive_file, dest)
            return

        tty.debug('Staging archive: {0}'.format(self.archive_file))

        if not self.archive_file:
            raise NoArchiveFileError(
                "Couldn't find archive file",
                "Failed on expand() for URL %s" % self.url)

        if not self.extension:
            self.extension = extension(self.url)

        if self.stage.expanded:
            tty.debug('Source already staged to %s' % self.stage.source_path)
            return

        decompress = decompressor_for(self.archive_file, self.extension)

        # Below we assume that the command to decompress expand the
        # archive in the current working directory
        with fs.exploding_archive_catch(self.stage):
            decompress(self.archive_file)

    def archive(self, destination):
        """Just moves this archive to the destination."""
        if not self.archive_file:
            raise NoArchiveFileError("Cannot call archive() before fetching.")

        spack.util.web.push_to_url(
            self.archive_file,
            destination,
            keep_original=True)

    @_needs_stage
    def check(self):
        """Check the downloaded archive against a checksum digest.
           No-op if this stage checks code out of a repository."""
        if not self.digest:
            raise NoDigestError(
                "Attempt to check URLFetchStrategy with no digest.")

        checker = crypto.Checker(self.digest)
        if not checker.check(self.archive_file):
            raise ChecksumError(
                "%s checksum failed for %s" %
                (checker.hash_name, self.archive_file),
                "Expected %s but got %s" % (self.digest, checker.sum))

    @_needs_stage
    def reset(self):
        """
        Removes the source path if it exists, then re-expands the archive.
        """
        if not self.archive_file:
            raise NoArchiveFileError(
                "Tried to reset URLFetchStrategy before fetching",
                "Failed on reset() for URL %s" % self.url)

        # Remove everything but the archive from the stage
        for filename in os.listdir(self.stage.path):
            abspath = os.path.join(self.stage.path, filename)
            if abspath != self.archive_file:
                shutil.rmtree(abspath, ignore_errors=True)

        # Expand the archive again
        self.expand()

    def __repr__(self):
        url = self.url if self.url else "no url"
        return "%s<%s>" % (self.__class__.__name__, url)

    def __str__(self):
        if self.url:
            return self.url
        else:
            return "[no url]"


@fetcher
class CacheURLFetchStrategy(URLFetchStrategy):
    """The resource associated with a cache URL may be out of date."""

    @_needs_stage
    def fetch(self):
        reg_str = r'^file://'
        path = re.sub(reg_str, '', self.url)

        # check whether the cache file exists.
        if not os.path.isfile(path):
            raise NoCacheError('No cache of %s' % path)

        # remove old symlink if one is there.
        filename = self.stage.save_filename
        if os.path.exists(filename):
            os.remove(filename)

        # Symlink to local cached archive.
        symlink(path, filename)

        # Remove link if checksum fails, or subsequent fetchers
        # will assume they don't need to download.
        if self.digest:
            try:
                self.check()
            except ChecksumError:
                os.remove(self.archive_file)
                raise

        # Notify the user how we fetched.
        tty.msg('Using cached archive: {0}'.format(path))


class VCSFetchStrategy(FetchStrategy):
    """Superclass for version control system fetch strategies.

    Like all fetchers, VCS fetchers are identified by the attributes
    passed to the ``version`` directive.  The optional_attrs for a VCS
    fetch strategy represent types of revisions, e.g. tags, branches,
    commits, etc.

    The required attributes (git, svn, etc.) are used to specify the URL
    and to distinguish a VCS fetch strategy from a URL fetch strategy.

    """

    def __init__(self, **kwargs):
        super(VCSFetchStrategy, self).__init__(**kwargs)

        # Set a URL based on the type of fetch strategy.
        self.url = kwargs.get(self.url_attr, None)
        if not self.url:
            raise ValueError(
                "%s requires %s argument." % (self.__class__, self.url_attr))

        for attr in self.optional_attrs:
            setattr(self, attr, kwargs.get(attr, None))

    @_needs_stage
    def check(self):
        tty.debug('No checksum needed when fetching with {0}'
                  .format(self.url_attr))

    @_needs_stage
    def expand(self):
        tty.debug(
            "Source fetched with %s is already expanded." % self.url_attr)

    @_needs_stage
    def archive(self, destination, **kwargs):
        assert (extension(destination) == 'tar.gz')
        assert (self.stage.source_path.startswith(self.stage.path))

        tar = which('tar', required=True)

        patterns = kwargs.get('exclude', None)
        if patterns is not None:
            if isinstance(patterns, six.string_types):
                patterns = [patterns]
            for p in patterns:
                tar.add_default_arg('--exclude=%s' % p)

        with working_dir(self.stage.path):
            if self.stage.srcdir:
                # Here we create an archive with the default repository name.
                # The 'tar' command has options for changing the name of a
                # directory that is included in the archive, but they differ
                # based on OS, so we temporarily rename the repo
                with temp_rename(self.stage.source_path, self.stage.srcdir):
                    tar('-czf', destination, self.stage.srcdir)
            else:
                tar('-czf', destination,
                    os.path.basename(self.stage.source_path))

    def __str__(self):
        return "VCS: %s" % self.url

    def __repr__(self):
        return "%s<%s>" % (self.__class__, self.url)


@fetcher
class GoFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that employs the `go get` infrastructure.

    Use like this in a package:

       version('name',
               go='github.com/monochromegane/the_platinum_searcher/...')

    Go get does not natively support versions, they can be faked with git.

    The fetched source will be moved to the standard stage sourcepath directory
    during the expand step.
    """
    url_attr = 'go'

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next
        # call to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(GoFetchStrategy, self).__init__(**forwarded_args)

        self._go = None

    @property
    def go_version(self):
        vstring = self.go('version', output=str).split(' ')[2]
        return spack.version.Version(vstring)

    @property
    def go(self):
        if not self._go:
            self._go = which('go', required=True)
        return self._go

    @_needs_stage
    def fetch(self):
        tty.debug('Getting go resource: {0}'.format(self.url))

        with working_dir(self.stage.path):
            try:
                os.mkdir('go')
            except OSError:
                pass
            env = dict(os.environ)
            env['GOPATH'] = os.path.join(os.getcwd(), 'go')
            self.go('get', '-v', '-d', self.url, env=env)

    def archive(self, destination):
        super(GoFetchStrategy, self).archive(destination, exclude='.git')

    @_needs_stage
    def expand(self):
        tty.debug(
            "Source fetched with %s is already expanded." % self.url_attr)

        # Move the directory to the well-known stage source path
        repo_root = _ensure_one_stage_entry(self.stage.path)
        shutil.move(repo_root, self.stage.source_path)

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.source_path):
            self.go('clean')

    def __str__(self):
        return "[go] %s" % self.url


@six.add_metaclass(abc.ABCMeta)
class GitRef(object):
    """A wrapper that knows how to format git refspecs in multiple contexts."""
    known_types = ['Branch', 'Commit', 'Tag']  # type: ClassVar[List[str]]
    ref_type = None                            # type: ClassVar[str]
    _ref = None                                # type: str

    Commit = None             # type: ClassVar[Type[GitCommit]]
    Tag = None                # type: ClassVar[Type[GitTag]]
    Branch = None             # type: ClassVar[Type[GitBranch]]

    def __init__(self, ref):
        # type: (str) -> None
        if self.ref_type not in self.known_types:
            # This is made a TypeError and not an InvalidGitRef because it cannot arise
            # from invalid user input.
            raise TypeError('GitRef can only have the types {0}, but was given {1!r}'
                            .format(self.known_types, self.ref_type))

        if not isinstance(ref, six.string_types):
            # This case can arise from user error when editing package.py files, so we
            # want to catch this and handle it specially to provide more context.
            raise InvalidGitRef('git reference was not a string: {0!r}'.format(ref))
        self._ref = ref

    def __repr__(self):
        return '{0}(ref_type={1!r}, ref={2!r})'.format(type(self).__name__,
                                                       self.ref_type, self._ref)

    def __str__(self):
        return '<{0}>'.format(self.repo_info_for_reference())

    def __eq__(self, other):
        # type: (Any) -> bool
        assert isinstance(other, GitRef)
        assert self.ref_type == other.ref_type, (self, other)
        return self._ref == other._ref

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self == other

    def unwrap(self):
        # type: () -> str
        """Extract the string underlying this GitRef instance.

        For use in testing. In general, methods should be exposed on the GitRepo class
        to operate on GitRef instances or specific subclasses instead of extracting this
        string."""
        return self._ref

    @abc.abstractmethod
    def should_validate_matches_hash(self):
        # type: () -> Optional[str]
        """Return a hash prefix that the repo checkout should be compared against."""

    @classmethod
    def from_version_directive(cls, kwargs):
        # type: (Dict) -> GitRef
        # (1) Extract the relevant arguments.
        commit = kwargs.pop('commit', None)
        tag = kwargs.pop('tag', None)
        branch = kwargs.pop('branch', None)
        version_name = kwargs.pop('version_name', None)
        # (2) Ensure no mutually exclusive kwargs are provided.
        num_specified = len(list(filter(None, [commit, tag, branch])))
        # (3) If no explicit git ref arguments are provided, assume that the version
        # string itself is to be used as the branch name. Ensure the version_name is
        # not blank.
        if (num_specified == 0) and version_name:
            return cls.Branch(version_name)
        # (4) If we are given a tag or a branch with a commit sha, note that by using
        # a special constructor.
        if num_specified == 2:
            if tag and commit:
                return cls.Tag(tag, commit=commit)
            if branch and commit:
                return cls.Branch(branch, commit=commit)
        # (5) If we don't have exactly one argument here, we have ambiguous ref
        # arguments, or no ref arguments at all, so error.
        if num_specified != 1:
            raise InvalidGitRef(dedent("""\
            A 'commit' hash prefix may be provided on its own, or in addition to either
            'tag' or branch' to ensure that the 'commit' hash prefix matches the tag or
            branch's actual hash after fetching. 'tag' and 'branch' are
            mutually exclusive.
            Given:
            commit={0}
            tag={1}
            branch={2}
            """).format(commit, tag, branch))
        # (6) Handle one-argument cases.
        if commit is not None:
            return cls.Commit(commit)
        if tag is not None:
            return cls.Tag(tag)
        assert branch is not None, (commit, tag, branch, version_name)
        return cls.Branch(branch)

    def refspec(self):
        # type: () -> str
        """Return a string which unambiguously identifies this ref to git."""
        if self.ref_type == 'Commit':
            return self._ref
        if self.ref_type == 'Tag':
            return 'refs/tags/{0}'.format(self._ref)
        assert self.ref_type == 'Branch', self
        return 'refs/heads/{0}'.format(self._ref)

    def fetch_spec(self):
        # type: () -> str
        """Return an argument to update a local ref from the remote, if applicable."""
        if self.ref_type == 'Commit':
            # Commits cannot be updated and do not require any special syntax to fetch.
            return self.refspec()
        # Otherwise, we use the syntax to update the local ref from a remote ref of
        # the same name, fetching updates if available/applicable.
        assert self.ref_type in ['Tag', 'Branch'], self
        maybe_mutating_prefix = '+' if self.is_mutable() else ''
        return '{0}{1}:{1}'.format(maybe_mutating_prefix, self.refspec())

    def is_mutable(self):
        # type: () -> bool
        """Whether this type of git ref should check for updates to that ref."""
        if self.ref_type == 'Branch':
            return True
        assert self.ref_type in ['Tag', 'Commit'], self
        return False

    def _repo_info(self):
        # type: () -> str
        if self.ref_type == 'Commit':
            return 'at commit {0}'.format(self._ref)
        if self.ref_type == 'Tag':
            return 'at tag {0}'.format(self._ref)
        assert self.ref_type == 'Branch', self
        return 'on branch {0}'.format(self._ref)

    def repo_info_for_reference(self):
        # type: () -> str
        if self.should_validate_matches_hash():
            return '{} (at commit {})'.format(
                self._repo_info(), self.should_validate_matches_hash())
        return self._repo_info()


class GitCommit(GitRef):
    """A git commit."""

    ref_type = 'Commit'        # type: ClassVar[str]

    # Matches any 7-40 character hexadecimal string.
    _commit_rx = re.compile(r'^[0-9a-f]{7,40}$', flags=re.IGNORECASE)

    def should_validate_matches_hash(self):
        # type: () -> Optional[str]
        """There is no need to verify that a git commit hash matches itself."""
        return None

    def matches_hash(self, ref):
        # type: (GitRef) -> bool
        hash_prefix = ref.should_validate_matches_hash()
        if hash_prefix is None:
            return True
        return self._ref.startswith(hash_prefix)

    def __hash__(self):
        return hash(self._ref)

    def __eq__(self, other):
        assert isinstance(other, GitCommit)
        return self._ref == other._ref

    def __ne__(self, other):
        return not self == other

    def __init__(self, ref):
        # type: (str) -> None
        if not isinstance(ref, six.string_types):
            # The exception message from `re.match()` does not print the value when
            # a non-string argument is provided, so we special-case that check here.
            raise InvalidGitRef('git reference was not a string: {0}'.format(ref))
        if not self._commit_rx.match(ref):
            raise InvalidGitRef(dedent("""\
            Spack requires that references to individual git commits be specified via
            a 7-40 character hexadecimal string, but received {0!r} instead.

            A valid commit hash case-insensitively matches the regular expression '{1}'.
            7 hex characters is the size printed out by `git log --format='%h'`, while
            40 hex characters is the size printed out by `git log --format='%H'`.
            """.format(ref, self._commit_rx.pattern)))
        super(GitCommit, self).__init__(ref)
GitRef.Commit = GitCommit       # noqa: E305


class GitTag(GitRef):
    """A git tag."""

    ref_type = 'Tag'        # type: ClassVar[str]

    @property
    def version(self):
        # type: () -> spack.version.Version
        return spack.version.Version(self._ref)

    def should_validate_matches_hash(self):
        # type: () -> Optional[str]
        return self._commit

    def create_tag_spec(self):
        # type: () -> str
        """Produce the string necessary to create a new tag."""
        return self._ref

    def __init__(self, ref, commit=None):
        # type: (str, Optional[str]) -> None
        super(GitTag, self).__init__(ref)
        self._commit = commit

    def __repr__(self):
        return 'GitTag(ref={!r}, commit={!r})'.format(self._ref, self._commit)

GitRef.Tag = GitTag             # noqa: E305


class GitBranch(GitRef):
    """A git branch."""

    ref_type = 'Branch'        # type: ClassVar[str]

    def should_validate_matches_hash(self):
        # type: () -> Optional[str]
        return self._commit

    def __init__(self, ref, commit=None):
        # type: (str, Optional[str]) -> None
        super(GitBranch, self).__init__(ref)
        self._commit = commit

    def __repr__(self):
        return 'GitBranch(ref={!r}, commit={!r})'.format(self._ref, self._commit)

GitRef.Branch = GitBranch       # noqa: E305


_SubmodulesType = Union[bool, 'Callable[[PackageBase], List[str]]']


class GitFetchStageConfiguration(object):
    """Validate parameters used to customize a specific git fetch operation.

    This information is orthogonal to that which is processed in `GitRef`. It describes
    what operations are performed to *prepare* a git checkout for a spack `Stage`,
    *after* fetching the configured ref.
    """
    submodules = None           # type: _SubmodulesType
    submodules_delete = None    # type: Optional[List[str]]
    get_full_repo = None        # type: bool

    def __repr__(self):
        return '{0}(submodules={1}, submodules_delete={2}, get_full_repo={3})'.format(
            type(self).__name__,
            self.submodules,
            self.submodules_delete,
            self.get_full_repo,
        )

    def __init__(self, submodules, submodules_delete, get_full_repo):
        # type: (_SubmodulesType, Optional[List[str]], bool) -> None
        self.submodules = submodules
        self.submodules_delete = submodules_delete
        self.get_full_repo = get_full_repo

    @classmethod
    def _extract_bool(cls, kwargs, name, default):
        # type: (Any, str, bool) -> bool
        value = kwargs.pop(name, default)
        if isinstance(value, bool):
            return value
        raise InvalidGitFetchStageConfig(
            'argument {0}={1!r} must be a bool'.format(name, value))

    @classmethod
    def _extract_bool_or_callable(cls, kwargs, name, default):
        # type: (Any, str, _SubmodulesType) -> _SubmodulesType
        value = kwargs.pop(name, default)
        if isinstance(value, bool) or callable(value):
            return value
        raise InvalidGitFetchStageConfig(
            'argument {0}={1!r} must be a bool or callable'.format(name, value))

    @classmethod
    def _extract_list(cls, kwargs, name, default):
        # type: (Any, str, Optional[List[str]]) -> Optional[List[str]]
        value = kwargs.pop(name, default)
        if isinstance(value, (list, type(None))):
            return value
        raise InvalidGitFetchStageConfig(
            'argument {0}={1!r} must be a list of str or None'
            .format(name, value))

    @classmethod
    def from_version_directive(cls, kwargs):
        # type: (Any) -> GitFetchStageConfiguration
        try:
            submodules = cls._extract_bool_or_callable(kwargs, 'submodules', False)
            submodules_delete = cls._extract_list(kwargs, 'submodules_delete', None)
            get_full_repo = cls._extract_bool(kwargs, 'get_full_repo', False)
        except InvalidGitFetchStageConfig as e:
            raise six.raise_from(  # type: ignore[attr-defined]
                InvalidGitFetchStageConfig(
                    'failed to parse {0} from kwargs {1}: {2}'
                    .format(cls.__name__, kwargs, e)),
                e,
            )                   # type: ignore[func-returns-value]
        return cls(submodules=submodules,
                   submodules_delete=submodules_delete,
                   get_full_repo=get_full_repo)


class ConfiguredGit(object):
    """Caches the version for the `git` executable, and adds compatibility args.

    Use the `.from_executable()` method to perform this checking:

        from spack.fetch_strategy import ConfiguredGit
        from spack.util.Executable import which

        git = ConfiguredGit.from_executable(which('git', required=True))
        assert git.version == '2.31.1'

    And note that the `__call__` method delegates to the inner executable from `which`:

        assert git('--version', output=str) == 'git version 2.31.1'
    """
    git = None                 # type: Executable
    version = None             # type: spack.version.Version

    def __init__(self, git, version):
        # type: (Executable, spack.version.Version) -> None
        self.git = git
        self.version = version

    def __repr__(self):
        return '{0}(git={1!r}, version={2!r})'.format(
            type(self).__name__, self.git, self.version)

    def __call__(self, *args, **kwargs):
        # type: (Any, Any) -> str
        """Execute `git`."""
        return cast(str, self.git(*args, **kwargs))

    def with_debug_output(self, *args, **kwargs):
        # type: (Any, Any) -> str
        """Execute `git`, teeing the output into `tty.debug()`."""
        output = cast(str, self(*args, output=str, error=str, **kwargs))
        tty.debug(output)
        return output

    _apple_git_suffix_rx = re.compile(r' +.*$')

    @classmethod
    def _strip_apple_git_suffix(cls, version_output):
        # type: (str) -> spack.version.Version
        """If there are any spaces, strip them out along with everything after them."""
        vstring = cls._apple_git_suffix_rx.sub('', version_output)
        return spack.version.Version(vstring)

    @classmethod
    def _get_git_version(cls, git):
        # type: (Executable) -> spack.version.Version
        vstring = cast(str, git('--version', output=str)).lstrip('git version ')
        return cls._strip_apple_git_suffix(vstring)

    @classmethod
    @lang.memoized
    def from_executable(cls, git):
        # type: (Executable) -> ConfiguredGit
        """Extract the version from a git executable and add defaults for compatibility.

        This method being `@memoized` means that with the current implementation of
        `Executable.__eq__`, any two `Executable` instances pointing to the same
        executable file path will return a cached result from this method, which will
        avoid executing the git process to obtain the version again.
        """
        version = cls._get_git_version(git)

        # Avoid any stderr message about a detached HEAD.
        # https://github.com/git/git/blob/master/Documentation/RelNotes/1.7.2.txt
        if version >= spack.version.Version('1.7.2'):
            git.add_default_arg('-c')
            git.add_default_arg('advice.detachedHead=false')

        # If the user asked for insecure fetching, make that work
        # with git as well.
        if not spack.config.get('config:verify_ssl'):
            git.add_default_env('GIT_SSL_NO_VERIFY', 'true')

        # Avoid trying to sign commits when using git for testing.
        git.add_default_arg('-c')
        git.add_default_arg('commit.gpgsign=false')

        return cls(git, version)


class GitRepo(object):
    """An instance of `ConfiguredGit`, confined to a specific repo.

    This class removes the chance of running a git command in the wrong repo by wrapping
    invocations of `__call__` and setting the working directory to the provided
    repo path.
    """
    git = None                  # type: ConfiguredGit
    repo_path = None            # type: str

    def __init__(self, git, repo_path):
        # type: (ConfiguredGit, str) -> None
        self.git = git
        self.repo_path = repo_path

    def __repr__(self):
        return '{0}(git={1!r}, repo_path={2!r})'.format(
            type(self).__name__, self.git, self.repo_path)

    def __call__(self, *args, **kwargs):
        # type: (Any, Any) -> str
        """Execute `git`, within `self.repo_path`."""
        with working_dir(self.repo_path):
            return self.git(*args, **kwargs)

    def with_debug_output(self, *args, **kwargs):
        # type: (Any, Any) -> str
        """Execute `git`, within `self.repo_path`, teeing it into tty.debug()."""
        with working_dir(self.repo_path):
            return self.git.with_debug_output(*args, **kwargs)

    _branch_listing_rx = re.compile(r'^refs/heads/(.*)$')

    def _iter_branches(self):
        # type: () -> Iterator[GitBranch]
        """Iterate over the names of all branches in this git repository.

        The first element of the yielded tuples corresponds to whether the branch was
        HEAD, and the second element is the branch itself."""
        # Can add %(HEAD) to the --format pattern to check whether each branch in turn
        # is HEAD by adding an asterisk or not. We don't currently require this
        # capability, since we maintain a separate git worktree per fetched version()
        # (e.g. each branch) of a package.
        for line in (self('branch', '--format=%(refname)',
                          output=str, fail_on_error=False)
                     .splitlines()):
            match = self._branch_listing_rx.match(line)
            assert match is not None, line
            (branch_name,) = match.groups()
            yield GitRef.Branch(branch_name)

    def branches_for(self):
        # type: () -> List[GitBranch]
        """List all branches in the repo, in arbitrary order."""
        return list(self._iter_branches())

    _tag_mapping_rx = re.compile(r'^([0-9a-f]{40}) refs/tags/(.*)$')

    def _iter_tags(self):
        # type: () -> Iterator[Tuple[GitCommit, GitTag]]
        for line in (self('for-each-ref', '--sort=creatordate',
                          '--format=%(objectname) %(refname)', 'refs/tags',
                          output=str)
                     .strip()
                     .splitlines()):
            tag_mapping_match = self._tag_mapping_rx.match(line)
            assert tag_mapping_match is not None
            tag_commit, tag = tag_mapping_match.groups()
            yield GitRef.Commit(tag_commit), GitRef.Tag(tag)

    def tags_for(self):
        # type: () -> List[Tuple[GitCommit, GitTag]]
        """List tags (with their commit hash) by date, with the newest at the bottom."""
        return list(self._iter_tags())

    def _iter_all_commits(self):
        # type: () -> Iterator[GitCommit]
        for line in (self('log', '--all', '--pretty=format:%H',
                          output=str)
                     .strip()
                     .splitlines()):
            yield GitRef.Commit(line)

    def all_commits_for(self):
        # type: () -> List[GitCommit]
        """List all commits in the repo, in reverse order."""
        return list(self._iter_all_commits())

    def _iter_head_commits(self):
        # type: () -> Iterator[GitCommit]
        for line in (self('rev-list', 'HEAD', output=str, error=str)
                     .strip()
                     .splitlines()):
            yield GitRef.Commit(line)

    def head_commits(self):
        # type: () -> List[GitCommit]
        """List all commits since HEAD, in reverse order."""
        return list(self._iter_head_commits())

    def calculate_ancestry_distance(self, a, b):
        # type: (GitRef, GitRef) -> Optional[int]
        self('merge-base', '--is-ancestor', a.refspec(), b.refspec(), ignore_errors=1)
        # TODO: thread-safe way to check returncode!
        if self.git.git.returncode != 0:
            return None
        return int(self('rev-list', '{0}..{1}'.format(a.refspec(), b.refspec()),
                        '--count',
                        output=str, error=str)
                   .strip())

    def expand_commit_hash(self, ref):
        # type: (GitRef) -> Optional[GitCommit]
        """Expands a ref into its full commit hash, or None if it does not exist."""
        check_commit_pattern = ref.refspec() + '^{commit}'
        try:
            return GitRef.Commit(
                self('rev-parse', '--verify', check_commit_pattern,
                     output=str, error=str)
                .strip())
        except ProcessError:
            return None

    def default_branch(self):
        # type: () -> GitBranch
        return GitRef.Branch(
            self('rev-parse', '--abbrev-ref', 'HEAD', output=str, error=str).strip(),
        )

    def config_set(self, key, value):
        # type: (str, str) -> None
        self.with_debug_output('config', key, value)

    def commit(self, message, date=None, autostage_modified=False, allow_empty=False):
        # type: (str, Optional[str], bool, bool) -> None
        empty_args = () if message else ('--allow-empty-message',)
        autostage_args = ('--all',) if autostage_modified else ()
        date_args = ('--date', date) if date else ()
        allow_empty_args = ('--allow-empty',) if allow_empty else ()
        message_args = ('-m', message)
        joined_args = (
            empty_args + autostage_args + date_args + allow_empty_args + message_args
        )
        self.with_debug_output('commit', *joined_args)

    def add(self, *files):
        # type: (str) -> None
        self.with_debug_output('add', *files)

    @staticmethod
    def protocol_supports_shallow_clone(remote_url):
        # type: (str) -> bool
        """Shallow clone operations (--depth #) are not supported by the basic
        HTTP protocol or by no-protocol file specifications.
        Use (e.g.) https:// or file:// instead."""
        scheme, _, _, _, _ = url_util.parse_git_url(remote_url)
        return not (scheme is None or scheme == 'http')

    def fetch(self, remote_url, ref, stage_config, verbose):
        # type: (str, GitRef, GitFetchStageConfiguration, bool) -> None
        """Fetch the specified ref from the specified remote into the current repo."""
        args = (
            'fetch',
            '--verbose' if verbose else '--quiet',
            '--recurse-submodules={0}'.format(
                'on-demand' if stage_config.submodules else 'no'),
        )

        # In the case of get_full_repo=True, we've already pulled down everything from
        # the remote, so we don't need to specify "--depth 1".
        depth_args = ()  # type: Tuple[str, ...]
        # If `get_full_repo=True`, first try to pull all new content down from the
        # remote without force-updating anything, and swallow any errors.
        if stage_config.get_full_repo:
            try:
                # The refspec will fetch all branches from the remote, while
                # '--tags' will fetch tags pointing into any of those branches.
                full_args = args + (
                    # If the checkout was previously a shallow one (with --depth 1),
                    # then pull all the relevant information down.
                    '--unshallow',
                    '--tags',
                    remote_url,
                    'refs/heads/*:refs/heads/*',
                )
                self.with_debug_output(*full_args)
            except ProcessError:
                # If a branch was force-updated so it can't be fast-forwarded, or if
                # a tag was modified at all upstream, then this `git fetch` call will
                # exit nonzero, but still do as much useful work as it can.
                pass
        else:
            # Since get_full_repo=None/False, we *do* want to avoid pulling down the
            # entire repo history if at all possible.
            if self.git.version >= spack.version.ver('1.7.1') and \
               self.protocol_supports_shallow_clone(remote_url):
                depth_args = ('--depth', '1')

        # Run `git fetch` again, ensuring that branches are updated from the remote even
        # if they cannot be fast-forwarded. Changing any tags upstream at all will raise
        # a FailedGitFetch.
        try:
            fetch_args = args + depth_args + (remote_url, ref.fetch_spec())
            self.with_debug_output(*fetch_args)
        except ProcessError as e:
            raise six.raise_from(  # type: ignore[attr-defined]
                FailedGitFetch(remote_url, ref, self, e),
                e,
            )                   # type: ignore[func-returns-value]

    def add_worktree(self, worktree_path, refspec, prune=True):
        # type: (str, str, bool) -> GitRepo
        # If the worktree directory already exists, assume it was already expanded.
        if os.path.isdir(worktree_path):
            return GitRepo(self.git, worktree_path)

        mkdirp(worktree_path)

        # `git worktree add -f` is necessary if the stage directory gets wiped, but
        # this leaves metadata around in the git repo pointing to missing worktrees.
        # `git worktree prune` avoids this.
        if prune:
            self.with_debug_output('worktree', 'prune')

        # Create a new worktree at the given ref, within the empty worktree directory.
        self.with_debug_output('worktree', 'add', worktree_path, refspec)

        return GitRepo(self.git, worktree_path)

    @staticmethod
    def _verbosity_args(verbose):
        # type: (bool) -> Tuple[str, ...]
        return () if verbose else ('--quiet',)

    def create_submodule(self, remote_url, clone_path):
        # type: (str, str) -> None
        self.with_debug_output('submodule', 'add', remote_url, clone_path)

    def update_submodules(self, submodules_arg, verbose=False):
        # type: (Union[bool, List[str]], bool) -> None
        if isinstance(submodules_arg, list):
            init_args = ('submodule', 'init', '--') + tuple(submodules_arg)
            self.with_debug_output(*init_args)
            update_args = ('submodule', 'update', '--recursive')
            self.with_debug_output(*update_args)
        else:
            args = ('submodule',) + self._verbosity_args(verbose=verbose) + (
                'update', '--init', '--recursive',
            )
            self.with_debug_output(*args)

    def delete_submodule(self, submodule_path, verbose=False):
        # type: (str, bool) -> None
        args = ('rm',) + self._verbosity_args(verbose=verbose) + (submodule_path,)
        self.with_debug_output(*args)

    def branch(self, branch):
        # type: (GitBranch) -> None
        """Create a new branch head named <branch> which points to the current HEAD."""
        self.with_debug_output('branch', branch.refspec())

    def checkout(
        self,
        ref=None,
        create=False,
    ):
        # type: (Optional[GitRef], bool) -> None
        """Check out <ref> without a detached HEAD warning.

        <ref> will default to a branch named `spack-internal-<uuid v4>`."""
        create_args = ('-b',) if create else ()
        ref = ref or GitRef.Branch('spack-internal-{0}'.format(uuid.uuid4()))
        joined_args = create_args + (ref.refspec(),)
        self.with_debug_output('checkout', *joined_args)

    def tag(self, tag):
        # type: (GitTag) -> None
        """Add a new tag reference named <tag>."""
        self.with_debug_output('tag', tag.create_tag_spec())

    @staticmethod
    def _ensure_repo_exists(git, repo_path):
        # type: (ConfiguredGit, str) -> None
        """Initialize a git repository at the given `repo_path` if it does not exist."""
        # Check whether the directory exists.
        if not os.path.isdir(repo_path):
            mkdirp(repo_path)
            tty.debug('Created directory at {0}'.format(repo_path))
        # If the '.git' directory does not exist, run `git init`.
        if os.path.isdir(os.path.join(repo_path, '.git')):
            tty.debug('Already initialized git repo at {0}'.format(repo_path))
        else:
            with working_dir(repo_path):
                git.with_debug_output('init')
            tty.debug('Newly initialized git repo at {0}'.format(repo_path))

    def _ensure_any_branch_exists(self):
        # type: () -> None
        """Create an initial empty commit and point a branch to it.

        This avoids pesky warning messages while executing git later.
        """
        if self.branches_for():
            return
        # To set a branch and make a commit without failing, we need to set a user.name
        # and user.email in this repository's config, in case it's not
        # configured globally.
        self.config_set('user.name', 'spack-internal-generated-user')
        self.config_set('user.email', 'spack-internal-generated-user@example.org')
        # `git branch` will only produce empty output immediately after `git
        # init` is run. In this case, we need to create a single ref guaranteed not to
        # collide with any branch name the user might want to check out, so we generate
        # a random UUID.
        self.checkout(create=True)
        # Creating a ref requires making a commit.
        self.commit('', allow_empty=True)

    @classmethod
    def initialize_idempotently(cls, git, repo_path):
        # type: (ConfiguredGit, str) -> GitRepo
        cls._ensure_repo_exists(git, repo_path)
        ret = cls(git, repo_path)
        ret._ensure_any_branch_exists()
        return ret


@fetcher
class GitFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that gets source code from a git repository.

    Use like this in a package:

        version('name', git='https://github.com/project/repo.git')

    Optionally, you can provide a branch, or commit to check out, e.g.:

        version('1.1', git='https://github.com/project/repo.git', tag='v1.1')

    You can use these three optional attributes in addition to ``git``:

        * ``branch``: Particular branch to build from (default is the
                      repository's default branch)
        * ``tag``: Particular tag to check out
        * ``commit``: Particular commit hash in the repo

    Repositories are cloned into the standard stage source path directory.
    """
    url_attr = 'git'
    optional_attrs = ['tag', 'branch', 'commit', 'version_name',
                      'submodules', 'get_full_repo', 'submodules_delete']

    # These fields are parsed from the constructor kwargs, i.e. the specified
    # `optional_attrs`.
    ref = None                  # type: GitRef
    stage_config = None         # type: GitFetchStageConfiguration

    git_version_re = r'git version (\S+)'

    def __init__(self, **kwargs):
        # type: (Any) -> None
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__.
        kwargs.pop('name', None)
        super(GitFetchStrategy, self).__init__(**kwargs)

        try:
            self.stage_config = (
                GitFetchStageConfiguration.from_version_directive(kwargs))
        except InvalidGitFetchStageConfig as e:
            raise six.raise_from(  # type: ignore[attr-defined]
                FetcherConflict(
                    'Failed to parse git fetch stage config '
                    'from the version() arguments {0}:\n\n{1}'.format(kwargs, e)),
                e,
            )                   # type: ignore[func-returns-value]

        try:
            self.ref = GitRef.from_version_directive(kwargs)
        except InvalidGitRef as e:
            raise six.raise_from(  # type: ignore[attr-defined]
                FetcherConflict(
                    'Failed to identify an unambiguous refspec '
                    '(commit, tag, or branch) '
                    'from the version() arguments {0}:\n\n{1}'.format(kwargs, e)),
                e,
            )                   # type: ignore[func-returns-value]

    @property                   # type: ignore[misc]
    @lang.memoized
    def canonical_git_repo(self):
        # type: () -> GitRepo
        """Lazily instantiate a GitRepo in the cache dir for this fetcher."""
        # Ensure git exists and configure it.
        git_exe = which('git', required=True)
        configured_git = ConfiguredGit.from_executable(git_exe)
        # Calculate the path to cache the git repo at.
        cache_path = spack.caches.fetch_cache.persistent_cache_dir_for(self)
        # Initialize the cached git repo.
        return GitRepo.initialize_idempotently(configured_git, cache_path)

    @property
    def cachable(self):
        # type: () -> bool
        return self.cache_enabled and not self.ref.is_mutable()

    def source_id(self):
        # type: () -> Optional[str]
        """Return the current refspec, when it points to an immutable object.

        A source id is supposed to be a reproducible source reference, which we can't
        have in the case of a branch."""
        if self.ref.is_mutable():
            return None
        return self.ref.refspec()

    def mirror_id(self):
        # type: () -> str
        repo_path = url_util.parse(self.url).path
        return os.path.sep.join(['git', repo_path, self.ref.refspec()])

    def _repo_info(self):
        # type: () -> str
        return '{0} {1}'.format(self.url, self.ref.repo_info_for_reference())

    def _maybe_expand_ref(self):
        # type: () -> Optional[GitCommit]
        """Return the full git hash for the current ref, if the ref exists locally."""
        return self.canonical_git_repo.expand_commit_hash(self.ref)

    def _do_fetch(self):
        # type: () -> GitCommit
        """Fetch the ref from the remote into the cache, then return the full git hash.

        This method checks that the ref successfully exists locally after fetching
        before returning.
        """
        verbose = bool(spack.config.get('config:debug'))
        self.canonical_git_repo.fetch(self.url, self.ref, self.stage_config,
                                      verbose=verbose)
        new_ref = self._maybe_expand_ref()
        assert new_ref is not None, (self.ref, self.canonical_git_repo)
        return new_ref

    def _ensure_local_ref(self):
        # type: () -> GitCommit
        """Fetch the ref specified by self.ref, and return its full git commit SHA."""
        current_expanded_ref = self._maybe_expand_ref()
        if current_expanded_ref is None:
            # We do not have the ref locally. Fetch it and check that it exists
            # after fetching.
            current_expanded_ref = self._do_fetch()
            tty.msg('Ref {0} -> {1} was newly downloaded from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref
        # We have the ref locally, and will not check for any updates.
        if not self.ref.is_mutable():
            tty.msg('Ref {0} -> {1} was already downloaded from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref

        # For branches which we have a previous copy of locally, we want to *attempt* to
        # fetch a newer version from the remote. If that fails, we continue to use the
        # locally-cached version.
        try:
            maybe_new_ref = self._do_fetch()
        except ProcessError as e:
            tty.warn(
                'Ref {0} -> {1} failed to update from {2} -- using local copy. '
                'The error was: {3}'
                .format(self.ref, current_expanded_ref, self.url, e))
            return current_expanded_ref
        # If we successfully fetched, print a nice message summarizing what kind of
        # update occurred, if any.
        if maybe_new_ref == current_expanded_ref:
            tty.msg('Ref {0} -> {1} did not have any updates from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref
        tty.msg('Ref {0} -> {1} was updated from previous value {2} at {3}.'
                .format(self.ref, maybe_new_ref, current_expanded_ref, self.url))
        return maybe_new_ref

    def _add_worktree(self, refspec):
        # type: (str) -> GitRepo
        """Checkout a worktree at `refspec` into the stage to form a `GitRepo`."""
        worktree_repo = self.canonical_git_repo.add_worktree(
            self.stage.source_path, refspec,
            prune=True)

        verbose = bool(spack.config.get('config:debug'))

        submodules = False  # type: Union[bool, List[str]]
        if self.stage_config.submodules:
            # We decided whether to fetch submodule info earlier, but this command
            # actually performs the update operations over the checked-out submodules.
            if callable(self.stage_config.submodules):
                submodules = self.stage_config.submodules(self.package)
            else:
                submodules = cast(bool, self.stage_config.submodules)
            worktree_repo.update_submodules(submodules, verbose=verbose)

            if self.stage_config.submodules_delete:
                for submodule_to_delete in self.stage_config.submodules_delete:
                    worktree_repo.delete_submodule(submodule_to_delete, verbose=verbose)

        return worktree_repo

    @_needs_stage
    def fetch(self):
        current_expanded_ref = self._ensure_local_ref()
        # In case the repo requires e.g. being checked out at a specific branch (and not
        # just a particular commit hash in a detached HEAD state), we provide the
        # refspec again to create the worktree.
        worktree_repo = self._add_worktree(self.ref.refspec())

        # If both a tag/branch as well as a commit is provided, ensure that, after
        # checking out the tag/branch, that it matches the commit SHA!
        if not current_expanded_ref.matches_hash(self.ref):
            raise InvalidGitRef(dedent("""\
            The given version provided the parameters: {}.
            The git checkout produced a commit {}, which did not match the commit
            hash prefix {}!
            """).format(self.ref, current_expanded_ref.unwrap(),
                        self.ref.should_validate_matches_hash()))

        # We use an `assert` here because this should never fail!
        assert (current_expanded_ref ==
                self.canonical_git_repo.expand_commit_hash(self.ref)), (
            current_expanded_ref, worktree_repo, self.ref,
                    self.canonical_git_repo.expand_commit_hash(self.ref))
        return True

    @_needs_stage
    def archive(self, destination):
        super(GitFetchStrategy, self).archive(destination, exclude='.git')

    @_needs_stage
    def reset(self):
        shutil.rmtree(self.stage.source_path, ignore_errors=True)
        self.fetch()

    def __str__(self):
        return '[git] {0}'.format(self._repo_info())


@fetcher
class CvsFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that gets source code from a CVS repository.
       Use like this in a package:

           version('name',
                   cvs=':pserver:anonymous@www.example.com:/cvsroot%module=modulename')

       Optionally, you can provide a branch and/or a date for the URL:

           version('name',
                   cvs=':pserver:anonymous@www.example.com:/cvsroot%module=modulename',
                   branch='branchname', date='date')

    Repositories are checked out into the standard stage source path directory.
    """
    url_attr = 'cvs'
    optional_attrs = ['branch', 'date']

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(CvsFetchStrategy, self).__init__(**forwarded_args)

        self._cvs = None
        if self.branch is not None:
            self.branch = str(self.branch)
        if self.date is not None:
            self.date = str(self.date)

    @property
    def cvs(self):
        if not self._cvs:
            self._cvs = which('cvs', required=True)
        return self._cvs

    @property
    def cachable(self):
        return self.cache_enabled and (bool(self.branch) or bool(self.date))

    def source_id(self):
        if not (self.branch or self.date):
            # We need a branch or a date to make a checkout reproducible
            return None
        id = 'id'
        if self.branch:
            id += '-branch=' + self.branch
        if self.date:
            id += '-date=' + self.date
        return id

    def mirror_id(self):
        if not (self.branch or self.date):
            # We need a branch or a date to make a checkout reproducible
            return None
        # Special-case handling because this is not actually a URL
        elements = self.url.split(':')
        final = elements[-1]
        elements = final.split('/')
        # Everything before the first slash is a port number
        elements = elements[1:]
        result = os.path.sep.join(['cvs'] + elements)
        if self.branch:
            result += '%branch=' + self.branch
        if self.date:
            result += '%date=' + self.date
        return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug('Already fetched {0}'.format(self.stage.source_path))
            return

        tty.debug('Checking out CVS repository: {0}'.format(self.url))

        with temp_cwd():
            url, module = self.url.split('%module=')
            # Check out files
            args = ['-z9', '-d', url, 'checkout']
            if self.branch is not None:
                args.extend(['-r', self.branch])
            if self.date is not None:
                args.extend(['-D', self.date])
            args.append(module)
            self.cvs(*args)
            # Rename repo
            repo_name = get_single_file('.')
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def _remove_untracked_files(self):
        """Removes untracked files in a CVS repository."""
        with working_dir(self.stage.source_path):
            status = self.cvs('-qn', 'update', output=str)
            for line in status.split('\n'):
                if re.match(r'^[?]', line):
                    path = line[2:].strip()
                    if os.path.isfile(path):
                        os.unlink(path)

    def archive(self, destination):
        super(CvsFetchStrategy, self).archive(destination, exclude='CVS')

    @_needs_stage
    def reset(self):
        self._remove_untracked_files()
        with working_dir(self.stage.source_path):
            self.cvs('update', '-C', '.')

    def __str__(self):
        return "[cvs] %s" % self.url


@fetcher
class SvnFetchStrategy(VCSFetchStrategy):

    """Fetch strategy that gets source code from a subversion repository.
       Use like this in a package:

           version('name', svn='http://www.example.com/svn/trunk')

       Optionally, you can provide a revision for the URL:

           version('name', svn='http://www.example.com/svn/trunk',
                   revision='1641')

    Repositories are checked out into the standard stage source path directory.
    """
    url_attr = 'svn'
    optional_attrs = ['revision']

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(SvnFetchStrategy, self).__init__(**forwarded_args)

        self._svn = None
        if self.revision is not None:
            self.revision = str(self.revision)

    @property
    def svn(self):
        if not self._svn:
            self._svn = which('svn', required=True)
        return self._svn

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = url_util.parse(self.url).path
            result = os.path.sep.join(['svn', repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug('Already fetched {0}'.format(self.stage.source_path))
            return

        tty.debug('Checking out subversion repository: {0}'.format(self.url))

        args = ['checkout', '--force', '--quiet']
        if self.revision:
            args += ['-r', self.revision]
        args.extend([self.url])

        with temp_cwd():
            self.svn(*args)
            repo_name = get_single_file('.')
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def _remove_untracked_files(self):
        """Removes untracked files in an svn repository."""
        with working_dir(self.stage.source_path):
            status = self.svn('status', '--no-ignore', output=str)
            self.svn('status', '--no-ignore')
            for line in status.split('\n'):
                if not re.match('^[I?]', line):
                    continue
                path = line[8:].strip()
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)

    def archive(self, destination):
        super(SvnFetchStrategy, self).archive(destination, exclude='.svn')

    @_needs_stage
    def reset(self):
        self._remove_untracked_files()
        with working_dir(self.stage.source_path):
            self.svn('revert', '.', '-R')

    def __str__(self):
        return "[svn] %s" % self.url


@fetcher
class HgFetchStrategy(VCSFetchStrategy):

    """
    Fetch strategy that gets source code from a Mercurial repository.
    Use like this in a package:

        version('name', hg='https://jay.grs.rwth-aachen.de/hg/lwm2')

    Optionally, you can provide a branch, or revision to check out, e.g.:

        version('torus',
                hg='https://jay.grs.rwth-aachen.de/hg/lwm2', branch='torus')

    You can use the optional 'revision' attribute to check out a
    branch, tag, or particular revision in hg.  To prevent
    non-reproducible builds, using a moving target like a branch is
    discouraged.

        * ``revision``: Particular revision, branch, or tag.

    Repositories are cloned into the standard stage source path directory.
    """
    url_attr = 'hg'
    optional_attrs = ['revision']

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(HgFetchStrategy, self).__init__(**forwarded_args)

        self._hg = None

    @property
    def hg(self):
        """
        Returns:
            Executable: the hg executable
        """
        if not self._hg:
            self._hg = which('hg', required=True)

            # When building PythonPackages, Spack automatically sets
            # PYTHONPATH. This can interfere with hg, which is a Python
            # script. Unset PYTHONPATH while running hg.
            self._hg.add_default_env('PYTHONPATH', '')

        return self._hg

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = url_util.parse(self.url).path
            result = os.path.sep.join(['hg', repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug('Already fetched {0}'.format(self.stage.source_path))
            return

        args = []
        if self.revision:
            args.append('at revision %s' % self.revision)
        tty.debug('Cloning mercurial repository: {0} {1}'
                  .format(self.url, args))

        args = ['clone']

        if not spack.config.get('config:verify_ssl'):
            args.append('--insecure')

        if self.revision:
            args.extend(['-r', self.revision])

        args.extend([self.url])

        with temp_cwd():
            self.hg(*args)
            repo_name = get_single_file('.')
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def archive(self, destination):
        super(HgFetchStrategy, self).archive(destination, exclude='.hg')

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.path):
            source_path = self.stage.source_path
            scrubbed = "scrubbed-source-tmp"

            args = ['clone']
            if self.revision:
                args += ['-r', self.revision]
            args += [source_path, scrubbed]
            self.hg(*args)

            shutil.rmtree(source_path, ignore_errors=True)
            shutil.move(scrubbed, source_path)

    def __str__(self):
        return "[hg] %s" % self.url


@fetcher
class S3FetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from an S3 bucket."""
    url_attr = 's3'

    def __init__(self, *args, **kwargs):
        try:
            super(S3FetchStrategy, self).__init__(*args, **kwargs)
        except ValueError as e:
            if not kwargs.get('url'):
                raise six.raise_from(
                    ValueError("S3FetchStrategy requires a url for fetching."),
                    e,
                )

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.debug('Already downloaded {0}'.format(self.archive_file))
            return

        parsed_url = url_util.parse(self.url)
        if parsed_url.scheme != 's3':
            raise FetchError(
                'S3FetchStrategy can only fetch from s3:// urls.')

        tty.debug('Fetching {0}'.format(self.url))

        basename = os.path.basename(parsed_url.path)

        with working_dir(self.stage.path):
            _, headers, stream = spack.util.web.read_from_url(self.url)

            with open(basename, 'wb') as f:
                shutil.copyfileobj(stream, f)

            content_type = spack.util.web.get_header(headers, 'Content-type')

        if content_type == 'text/html':
            warn_content_type_mismatch(self.archive_file or "the archive")

        if self.stage.save_filename:
            llnl.util.filesystem.rename(
                os.path.join(self.stage.path, basename),
                self.stage.save_filename)

        if not self.archive_file:
            raise FailedDownloadError(self.url)


@fetcher
class GCSFetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from a GCS bucket."""
    url_attr = 'gs'

    def __init__(self, *args, **kwargs):
        try:
            super(GCSFetchStrategy, self).__init__(*args, **kwargs)
        except ValueError:
            if not kwargs.get('url'):
                raise ValueError(
                    "GCSFetchStrategy requires a url for fetching.")

    @_needs_stage
    def fetch(self):
        import spack.util.web as web_util
        if self.archive_file:
            tty.debug('Already downloaded {0}'.format(self.archive_file))
            return

        parsed_url = url_util.parse(self.url)
        if parsed_url.scheme != 'gs':
            raise FetchError(
                'GCSFetchStrategy can only fetch from gs:// urls.')

        tty.debug('Fetching {0}'.format(self.url))

        basename = os.path.basename(parsed_url.path)

        with working_dir(self.stage.path):
            _, headers, stream = web_util.read_from_url(self.url)

            with open(basename, 'wb') as f:
                shutil.copyfileobj(stream, f)

            content_type = web_util.get_header(headers, 'Content-type')

        if content_type == 'text/html':
            warn_content_type_mismatch(self.archive_file or "the archive")

        if self.stage.save_filename:
            os.rename(
                os.path.join(self.stage.path, basename),
                self.stage.save_filename)

        if not self.archive_file:
            raise FailedDownloadError(self.url)


def stable_target(fetcher):
    """Returns whether the fetcher target is expected to have a stable
       checksum. This is only true if the target is a preexisting archive
       file."""
    if isinstance(fetcher, URLFetchStrategy) and fetcher.cachable:
        return True
    return False


def from_url(url):
    """Given a URL, find an appropriate fetch strategy for it.
       Currently just gives you a URLFetchStrategy that uses curl.

       TODO: make this return appropriate fetch strategies for other
             types of URLs.
    """
    return URLFetchStrategy(url)


def from_kwargs(**kwargs):
    """Construct an appropriate FetchStrategy from the given keyword arguments.

    Args:
        **kwargs: dictionary of keyword arguments, e.g. from a
            ``version()`` directive in a package.

    Returns:
        typing.Callable: The fetch strategy that matches the args, based
            on attribute names (e.g., ``git``, ``hg``, etc.)

    Raises:
        FetchError: If no ``fetch_strategy`` matches the args.
    """
    for fetcher in all_strategies:
        if fetcher.matches(kwargs):
            return fetcher(**kwargs)

    raise InvalidArgsError(**kwargs)


def check_pkg_attributes(pkg):
    """Find ambiguous top-level fetch attributes in a package.

    Currently this only ensures that two or more VCS fetch strategies are
    not specified at once.
    """
    # a single package cannot have URL attributes for multiple VCS fetch
    # strategies *unless* they are the same attribute.
    conflicts = set([s.url_attr for s in all_strategies
                     if hasattr(pkg, s.url_attr)])

    # URL isn't a VCS fetch method. We can use it with a VCS method.
    conflicts -= set(['url'])

    if len(conflicts) > 1:
        raise FetcherConflict(
            'Package %s cannot specify %s together. Pick at most one.'
            % (pkg.name, comma_and(quote(conflicts))))


def _check_version_attributes(fetcher, pkg, version):
    """Ensure that the fetcher for a version is not ambiguous.

    This assumes that we have already determined the fetcher for the
    specific version using ``for_package_version()``
    """
    all_optionals = set(a for s in all_strategies for a in s.optional_attrs)

    args = pkg.versions[version]
    extra\
        = set(args) - set(fetcher.optional_attrs) - \
        set([fetcher.url_attr, 'no_cache'])
    extra.intersection_update(all_optionals)

    if extra:
        legal_attrs = [fetcher.url_attr] + list(fetcher.optional_attrs)
        raise FetcherConflict(
            "%s version '%s' has extra arguments: %s"
            % (pkg.name, version, comma_and(quote(extra))),
            "Valid arguments for a %s fetcher are: \n    %s"
            % (fetcher.url_attr, comma_and(quote(legal_attrs))))


def _extrapolate(pkg, version):
    """Create a fetcher from an extrapolated URL for this version."""
    try:
        return URLFetchStrategy(pkg.url_for_version(version),
                                fetch_options=pkg.fetch_options)
    except spack.package_base.NoURLError as e:
        msg = ("Can't extrapolate a URL for version %s "
               "because package %s defines no URLs")
        raise six.raise_from(ExtrapolationError(msg % (version, pkg.name)), e)


def _from_merged_attrs(fetcher, pkg, version):
    """Create a fetcher from merged package and version attributes."""
    if fetcher.url_attr == 'url':
        mirrors = pkg.all_urls_for_version(version)
        url = mirrors[0]
        mirrors = mirrors[1:]
        attrs = {fetcher.url_attr: url, 'mirrors': mirrors}
    else:
        url = getattr(pkg, fetcher.url_attr)
        attrs = {fetcher.url_attr: url}

    attrs['fetch_options'] = pkg.fetch_options
    # version() directives may not explicitly provide any kwargs, and if this occurs
    # then the appropriate fetch strategy does not otherwise have access to the value of
    # the version() argument. Fetch strategies can accept 'version_name' in their
    # optional_attrs in order to be able to interpret bare version strings.
    attrs['version_name'] = str(version)
    attrs.update(pkg.versions[version])

    if fetcher.url_attr == 'git' and hasattr(pkg, 'submodules'):
        attrs.setdefault('submodules', pkg.submodules)

    return fetcher(**attrs)


def for_package_version(pkg, version):
    """Determine a fetch strategy based on the arguments supplied to
       version() in the package description."""

    # No-code packages have a custom fetch strategy to work around issues
    # with resource staging.
    if not pkg.has_code:
        return BundleFetchStrategy()

    check_pkg_attributes(pkg)

    if not isinstance(version, spack.version.VersionBase):
        version = spack.version.Version(version)

    # if it's a commit, we must use a GitFetchStrategy
    if isinstance(version, spack.version.GitVersion):
        if not hasattr(pkg, "git"):
            raise FetchError(
                "Cannot fetch git version for %s. Package has no 'git' attribute" %
                pkg.name
            )
        # Populate the version with comparisons to other commits
        version.generate_git_lookup(pkg.name)

        # For GitVersion, we have no way to determine whether a ref is a branch or tag
        # Fortunately, we handle branches and tags identically, except tags are
        # handled slightly more conservatively for older versions of git.
        # We call all non-commit refs tags in this context, at the cost of a slight
        # performance hit for branches on older versions of git.
        # Branches cannot be cached, so we tell the fetcher not to cache tags/branches
        ref_type = 'commit' if version.is_commit else 'tag'
        kwargs = {
            'git': pkg.git,
            ref_type: version.ref,
            'no_cache': True,
        }
        kwargs['submodules'] = getattr(pkg, 'submodules', False)
        fetcher = GitFetchStrategy(**kwargs)
        return fetcher

    # If it's not a known version, try to extrapolate one by URL
    if version not in pkg.versions:
        return _extrapolate(pkg, version)

    # Set package args first so version args can override them
    args = {'fetch_options': pkg.fetch_options}
    # Grab a dict of args out of the package version dict
    args.update(pkg.versions[version])

    # If the version specifies a `url_attr` directly, use that.
    for fetcher in all_strategies:
        if fetcher.url_attr in args:
            _check_version_attributes(fetcher, pkg, version)
            if fetcher.url_attr == 'git' and hasattr(pkg, 'submodules'):
                args.setdefault('submodules', pkg.submodules)
            return fetcher(**args)

    # if a version's optional attributes imply a particular fetch
    # strategy, and we have the `url_attr`, then use that strategy.
    for fetcher in all_strategies:
        if hasattr(pkg, fetcher.url_attr) or fetcher.url_attr == 'url':
            optionals = fetcher.optional_attrs
            if optionals and any(a in args for a in optionals):
                _check_version_attributes(fetcher, pkg, version)
                return _from_merged_attrs(fetcher, pkg, version)

    # if the optional attributes tell us nothing, then use any `url_attr`
    # on the package.  This prefers URL vs. VCS, b/c URLFetchStrategy is
    # defined first in this file.
    for fetcher in all_strategies:
        if hasattr(pkg, fetcher.url_attr):
            _check_version_attributes(fetcher, pkg, version)
            return _from_merged_attrs(fetcher, pkg, version)

    raise InvalidArgsError(pkg, version, **args)


def from_url_scheme(url, *args, **kwargs):
    """Finds a suitable FetchStrategy by matching its url_attr with the scheme
       in the given url."""

    url = kwargs.get('url', url)
    parsed_url = urllib_parse.urlparse(url, scheme='file')

    scheme_mapping = (
        kwargs.get('scheme_mapping') or
        {
            'file': 'url',
            'http': 'url',
            'https': 'url',
            'ftp': 'url',
            'ftps': 'url',
        })

    scheme = parsed_url.scheme
    scheme = scheme_mapping.get(scheme, scheme)

    for fetcher in all_strategies:
        url_attr = getattr(fetcher, 'url_attr', None)
        if url_attr and url_attr == scheme:
            return fetcher(url, *args, **kwargs)

    raise ValueError(
        'No FetchStrategy found for url with scheme: "{SCHEME}"'.format(
            SCHEME=parsed_url.scheme))


def from_list_url(pkg):
    """If a package provides a URL which lists URLs for resources by
       version, this can can create a fetcher for a URL discovered for
       the specified package's version."""

    if pkg.list_url:
        try:
            versions = pkg.fetch_remote_versions()
            try:
                # get a URL, and a checksum if we have it
                url_from_list = versions[pkg.version]
                checksum = None

                # try to find a known checksum for version, from the package
                version = pkg.version
                if version in pkg.versions:
                    args = pkg.versions[version]
                    checksum = next(
                        (v for k, v in args.items() if k in crypto.hashes),
                        args.get('checksum'))

                # construct a fetcher
                return URLFetchStrategy(url_from_list, checksum,
                                        fetch_options=pkg.fetch_options)
            except KeyError as e:
                tty.debug(e)
                tty.msg("Cannot find version %s in url_list" % pkg.version)

        except BaseException as e:
            # TODO: Don't catch BaseException here! Be more specific.
            tty.debug(e)
            tty.msg("Could not determine url from list_url.")


class FsCache(object):

    def __init__(self, root):
        self.root = os.path.abspath(root)

    # TODO: use this method to determine the cache path for CacheURLFetchStrategy too!
    def persistent_cache_dir_for(self, fetcher):
        url_components = os.path.sep.join(filter(None, url_util.parse(fetcher.url)))
        return os.path.join(self.root, fetcher.url_attr, url_components)

    def store(self, fetcher, relative_dest):
        # Skip fetchers that aren't cachable.
        if not fetcher.cachable:
            return

        # Don't store things that are already cached.
        if isinstance(fetcher, CacheURLFetchStrategy):
            return

        dst = os.path.join(self.root, relative_dest)
        mkdirp(os.path.dirname(dst))
        fetcher.archive(dst)

    def fetcher(self, target_path, digest, **kwargs):
        path = os.path.join(self.root, target_path)
        return CacheURLFetchStrategy(path, digest, **kwargs)

    def destroy(self):
        shutil.rmtree(self.root, ignore_errors=True)


class FetchError(spack.error.SpackError):
    """Superclass for fetcher errors."""


class NoCacheError(FetchError):
    """Raised when there is no cached archive for a package."""


class FailedDownloadError(FetchError):
    """Raised when a download fails."""
    def __init__(self, url, msg=""):
        super(FailedDownloadError, self).__init__(
            "Failed to fetch file from URL: %s" % url, msg)
        self.url = url


class NoArchiveFileError(FetchError):
    """"Raised when an archive file is expected but none exists."""


class NoDigestError(FetchError):
    """Raised after attempt to checksum when URL has no digest."""


class ExtrapolationError(FetchError):
    """Raised when we can't extrapolate a version for a package."""


class FetcherConflict(FetchError):
    """Raised for packages with invalid fetch attributes."""


class InvalidArgsError(FetchError):
    """Raised when a version can't be deduced from a set of arguments."""
    def __init__(self, pkg=None, version=None, **args):
        msg = "Could not guess a fetch strategy"
        if pkg:
            msg += ' for {pkg}'.format(pkg=pkg)
            if version:
                msg += '@{version}'.format(version=version)
        long_msg = 'with arguments: {args}'.format(args=args)
        super(InvalidArgsError, self).__init__(msg, long_msg)


class ChecksumError(FetchError):
    """Raised when archive fails to checksum."""


class NoStageError(FetchError):
    """Raised when fetch operations are called before set_stage()."""
    def __init__(self, method):
        super(NoStageError, self).__init__(
            "Must call FetchStrategy.set_stage() before calling %s" %
            method.__name__)


class InvalidGitRef(ValueError):
    """Raised internally when a single git version can't be deduced."""


class InvalidGitFetchStageConfig(ValueError):
    """Raised internally when git fetching parameters can't be parsed."""


class FailedGitFetch(FetchError):
    """Raised when git fails to fetch a ref for an unknown reason."""
    def __init__(self, remote_url, ref, git_repo, exc):
        # type: (str, GitRef, GitRepo, BaseException) -> None
        super(FailedGitFetch, self).__init__(
            "Failed to fetch ref {0} into repo {1} from remote: {2}"
            .format(ref, git_repo, remote_url),
            str(exc))
