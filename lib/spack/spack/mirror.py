# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This file contains code for creating spack mirror directories.  A
mirror is an organized hierarchy containing specially named archive
files.  This enabled spack to know where to find files in a mirror if
the main server for a particular package is down.  Or, if the computer
where spack is run is not connected to the internet, it allows spack
to download packages directly from a mirror (e.g., on an intranet).
"""
import collections
import collections.abc
import operator
import os
import os.path
import sys
import traceback
import urllib.parse

import ruamel.yaml.error as yaml_error

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.caches
import spack.config
import spack.error
import spack.fetch_strategy as fs
import spack.mirror
import spack.spec
import spack.url as url
import spack.util.path
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
from spack.util.spack_yaml import syaml_dict
from spack.version import VersionList

#: What schemes do we support
supported_url_schemes = ("file", "http", "https", "sftp", "ftp", "s3", "gs")


def _display_mirror_entry(size, name, url, type_=None):
    if type_:
        type_ = "".join((" (", type_, ")"))
    else:
        type_ = ""

    print("%-*s%s%s" % (size + 4, name, url, type_))


def _url_or_path_to_url(url_or_path: str) -> str:
    """For simplicity we allow mirror URLs in config files to be local, relative paths.
    This helper function takes care of distinguishing between URLs and paths, and
    canonicalizes paths before transforming them into file:// URLs."""
    # Is it a supported URL already? Then don't do path-related canonicalization.
    parsed = urllib.parse.urlparse(url_or_path)
    if parsed.scheme in supported_url_schemes:
        return url_or_path

    # Otherwise we interpret it as path, and we should promote it to file:// URL.
    return url_util.path_to_file_url(spack.util.path.canonicalize_path(url_or_path))


class Mirror(object):
    """Represents a named location for storing source tarballs and binary
    packages.

    Mirrors have a fetch_url that indicate where and how artifacts are fetched
    from them, and a push_url that indicate where and how artifacts are pushed
    to them. These two URLs are usually the same.
    """

    def __init__(self, fetch_url, push_url=None, name=None):
        self._fetch_url = fetch_url
        self._push_url = push_url
        self._name = name

    def __eq__(self, other):
        return self._fetch_url == other._fetch_url and self._push_url == other._push_url

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(), stream)

    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return Mirror.from_dict(data, name)
        except yaml_error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML mirror:", str(e)) from e

    @staticmethod
    def from_json(stream, name=None):
        try:
            d = sjson.load(stream)
            return Mirror.from_dict(d, name)
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON mirror:", str(e)) from e

    @staticmethod
    def from_local_path(path: str):
        return Mirror(fetch_url=url_util.path_to_file_url(path))

    @staticmethod
    def from_url(url: str):
        """Create an anonymous mirror by URL. This method validates the URL."""
        if not urllib.parse.urlparse(url).scheme in supported_url_schemes:
            raise ValueError(
                '"{}" is not a valid mirror URL. Scheme must be once of {}.'.format(
                    url, ", ".join(supported_url_schemes)
                )
            )
        return Mirror(fetch_url=url)

    def to_dict(self):
        # Keep it a key-value pair <name>: <url> when possible.
        if isinstance(self._fetch_url, str) and self._push_url is None:
            return self._fetch_url

        if self._push_url is None:
            return syaml_dict([("fetch", self._fetch_url), ("push", self._fetch_url)])
        else:
            return syaml_dict([("fetch", self._fetch_url), ("push", self._push_url)])

    @staticmethod
    def from_dict(d, name=None):
        if isinstance(d, str):
            return Mirror(d, name=name)
        else:
            return Mirror(d["fetch"], d["push"], name=name)

    def display(self, max_len=0):
        if self._push_url is None:
            _display_mirror_entry(max_len, self._name, self.fetch_url)
        else:
            _display_mirror_entry(max_len, self._name, self.fetch_url, "fetch")
            _display_mirror_entry(max_len, self._name, self.push_url, "push")

    def __str__(self):
        name = self._name
        if name is None:
            name = ""
        else:
            name = ' "%s"' % name

        if self._push_url is None:
            return "[Mirror%s (%s)]" % (name, self._fetch_url)

        return "[Mirror%s (fetch: %s, push: %s)]" % (name, self._fetch_url, self._push_url)

    def __repr__(self):
        return "".join(
            (
                "Mirror(",
                ", ".join(
                    "%s=%s" % (k, repr(v))
                    for k, v in (
                        ("fetch_url", self._fetch_url),
                        ("push_url", self._push_url),
                        ("name", self._name),
                    )
                    if k == "fetch_url" or v
                ),
                ")",
            )
        )

    @property
    def name(self):
        return self._name or "<unnamed>"

    def get_profile(self, url_type):
        if isinstance(self._fetch_url, dict):
            if url_type == "push":
                return self._push_url.get("profile", None)
            return self._fetch_url.get("profile", None)
        else:
            return None

    def set_profile(self, url_type, profile):
        if url_type == "push":
            self._push_url["profile"] = profile
        else:
            self._fetch_url["profile"] = profile

    def get_access_pair(self, url_type):
        if isinstance(self._fetch_url, dict):
            if url_type == "push":
                return self._push_url.get("access_pair", None)
            return self._fetch_url.get("access_pair", None)
        else:
            return None

    def set_access_pair(self, url_type, connection_tuple):
        if url_type == "push":
            self._push_url["access_pair"] = connection_tuple
        else:
            self._fetch_url["access_pair"] = connection_tuple

    def get_endpoint_url(self, url_type):
        if isinstance(self._fetch_url, dict):
            if url_type == "push":
                return self._push_url.get("endpoint_url", None)
            return self._fetch_url.get("endpoint_url", None)
        else:
            return None

    def set_endpoint_url(self, url_type, url):
        if url_type == "push":
            self._push_url["endpoint_url"] = url
        else:
            self._fetch_url["endpoint_url"] = url

    def get_access_token(self, url_type):
        if isinstance(self._fetch_url, dict):
            if url_type == "push":
                return self._push_url.get("access_token", None)
            return self._fetch_url.get("access_token", None)
        else:
            return None

    def set_access_token(self, url_type, connection_token):
        if url_type == "push":
            self._push_url["access_token"] = connection_token
        else:
            self._fetch_url["access_token"] = connection_token

    @property
    def fetch_url(self):
        """Get the valid, canonicalized fetch URL"""
        url_or_path = (
            self._fetch_url if isinstance(self._fetch_url, str) else self._fetch_url["url"]
        )
        return _url_or_path_to_url(url_or_path)

    @fetch_url.setter
    def fetch_url(self, url):
        self._fetch_url["url"] = url
        self._normalize()

    @property
    def push_url(self):
        """Get the valid, canonicalized push URL. Returns fetch URL if no custom
        push URL is defined"""
        if self._push_url is None:
            return self.fetch_url
        url_or_path = self._push_url if isinstance(self._push_url, str) else self._push_url["url"]
        return _url_or_path_to_url(url_or_path)

    @push_url.setter
    def push_url(self, url):
        self._push_url["url"] = url
        self._normalize()

    def _normalize(self):
        if self._push_url is not None and self._push_url == self._fetch_url:
            self._push_url = None


class MirrorCollection(collections.abc.Mapping):
    """A mapping of mirror names to mirrors."""

    def __init__(self, mirrors=None, scope=None):
        self._mirrors = collections.OrderedDict(
            (name, Mirror.from_dict(mirror, name))
            for name, mirror in (
                mirrors.items()
                if mirrors is not None
                else spack.config.get("mirrors", scope=scope).items()
            )
        )

    def __eq__(self, other):
        return self._mirrors == other._mirrors

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(True), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(True), stream)

    # TODO: this isn't called anywhere
    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return MirrorCollection(data)
        except yaml_error.MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML mirror collection:", str(e)) from e

    @staticmethod
    def from_json(stream, name=None):
        try:
            d = sjson.load(stream)
            return MirrorCollection(d)
        except Exception as e:
            raise sjson.SpackJSONError("error parsing JSON mirror collection:", str(e)) from e

    def to_dict(self, recursive=False):
        return syaml_dict(
            sorted(
                ((k, (v.to_dict() if recursive else v)) for (k, v) in self._mirrors.items()),
                key=operator.itemgetter(0),
            )
        )

    @staticmethod
    def from_dict(d):
        return MirrorCollection(d)

    def __getitem__(self, item):
        return self._mirrors[item]

    def display(self):
        max_len = max(len(mirror.name) for mirror in self._mirrors.values())
        for mirror in self._mirrors.values():
            mirror.display(max_len)

    def lookup(self, name_or_url):
        """Looks up and returns a Mirror.

        If this MirrorCollection contains a named Mirror under the name
        [name_or_url], then that mirror is returned.  Otherwise, [name_or_url]
        is assumed to be a mirror URL, and an anonymous mirror with the given
        URL is returned.
        """
        result = self.get(name_or_url)

        if result is None:
            result = Mirror(fetch_url=name_or_url)

        return result

    def __iter__(self):
        return iter(self._mirrors)

    def __len__(self):
        return len(self._mirrors)


def _determine_extension(fetcher):
    if isinstance(fetcher, fs.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = url.determine_url_file_extension(fetcher.url)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip(".")
            else:
                msg = """\
Unable to parse extension from {0}.

If this URL is for a tarball but does not include the file extension
in the name, you can explicitly declare it with the following syntax:

    version('1.2.3', 'hash', extension='tar.gz')

If this URL is for a download like a .jar or .whl that does not need
to be expanded, or an uncompressed installation script, you can tell
Spack not to expand it with the following syntax:

    version('1.2.3', 'hash', expand=False)
"""
                raise MirrorError(msg.format(fetcher.url))
        else:
            # If the archive shouldn't be expanded, don't check extension.
            ext = None
    else:
        # Otherwise we'll make a .tar.gz ourselves
        ext = "tar.gz"

    return ext


class MirrorReference(object):
    """A ``MirrorReference`` stores the relative paths where you can store a
    package/resource in a mirror directory.

    The appropriate storage location is given by ``storage_path``. The
    ``cosmetic_path`` property provides a reference that a human could generate
    themselves based on reading the details of the package.

    A user can iterate over a ``MirrorReference`` object to get all the
    possible names that might be used to refer to the resource in a mirror;
    this includes names generated by previous naming schemes that are no-longer
    reported by ``storage_path`` or ``cosmetic_path``.
    """

    def __init__(self, cosmetic_path, global_path=None):
        self.global_path = global_path
        self.cosmetic_path = cosmetic_path

    @property
    def storage_path(self):
        if self.global_path:
            return self.global_path
        else:
            return self.cosmetic_path

    def __iter__(self):
        if self.global_path:
            yield self.global_path
        yield self.cosmetic_path


def mirror_archive_paths(fetcher, per_package_ref, spec=None):
    """Returns a ``MirrorReference`` object which keeps track of the relative
    storage path of the resource associated with the specified ``fetcher``."""
    ext = None
    if spec:
        pkg_cls = spack.repo.path.get_pkg_class(spec.name)
        versions = pkg_cls.versions.get(spec.version, {})
        ext = versions.get("extension", None)
    # If the spec does not explicitly specify an extension (the default case),
    # then try to determine it automatically. An extension can only be
    # specified for the primary source of the package (e.g. the source code
    # identified in the 'version' declaration). Resources/patches don't have
    # an option to specify an extension, so it must be inferred for those.
    ext = ext or _determine_extension(fetcher)

    if ext:
        per_package_ref += ".%s" % ext

    global_ref = fetcher.mirror_id()
    if global_ref:
        global_ref = os.path.join("_source-cache", global_ref)
    if global_ref and ext:
        global_ref += ".%s" % ext

    return MirrorReference(per_package_ref, global_ref)


def get_all_versions(specs):
    """Given a set of initial specs, return a new set of specs that includes
    each version of each package in the original set.

    Note that if any spec in the original set specifies properties other than
    version, this information will be omitted in the new set; for example; the
    new set of specs will not include variant settings.
    """
    version_specs = []
    for spec in specs:
        pkg_cls = spack.repo.path.get_pkg_class(spec.name)
        # Skip any package that has no known versions.
        if not pkg_cls.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg_cls.name)
            continue

        for version in pkg_cls.versions:
            version_spec = spack.spec.Spec(pkg_cls.name)
            version_spec.versions = VersionList([version])
            version_specs.append(version_spec)

    return version_specs


def get_matching_versions(specs, num_versions=1):
    """Get a spec for EACH known version matching any spec in the list.
    For concrete specs, this retrieves the concrete version and, if more
    than one version per spec is requested, retrieves the latest versions
    of the package.
    """
    matching = []
    for spec in specs:
        pkg = spec.package

        # Skip any package that has no known versions.
        if not pkg.versions:
            tty.msg("No safe (checksummed) versions for package %s" % pkg.name)
            continue

        pkg_versions = num_versions

        version_order = list(reversed(sorted(pkg.versions)))
        matching_spec = []
        if spec.concrete:
            matching_spec.append(spec)
            pkg_versions -= 1
            if spec.version in version_order:
                version_order.remove(spec.version)

        for v in version_order:
            # Generate no more than num_versions versions for each spec.
            if pkg_versions < 1:
                break

            # Generate only versions that satisfy the spec.
            if spec.concrete or v.intersects(spec.versions):
                s = spack.spec.Spec(pkg.name)
                s.versions = VersionList([v])
                s.variants = spec.variants.copy()
                # This is needed to avoid hanging references during the
                # concretization phase
                s.variants.spec = s
                matching_spec.append(s)
                pkg_versions -= 1

        if not matching_spec:
            tty.warn("No known version matches spec: %s" % spec)
        matching.extend(matching_spec)

    return matching


def create(path, specs, skip_unstable_versions=False):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.
    """
    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, spack.spec.Spec) else spack.spec.Spec(s) for s in specs]

    mirror_cache, mirror_stats = mirror_cache_and_stats(path, skip_unstable_versions)
    for spec in specs:
        mirror_stats.next_spec(spec)
        create_mirror_from_package_object(spec.package, mirror_cache, mirror_stats)

    return mirror_stats.stats()


def mirror_cache_and_stats(path, skip_unstable_versions=False):
    """Return both a mirror cache and a mirror stats, starting from the path
    where a mirror ought to be created.

    Args:
        path (str): path to create a mirror directory hierarchy in.
        skip_unstable_versions: if true, this skips adding resources when
            they do not have a stable archive checksum (as determined by
            ``fetch_strategy.stable_target``)
    """
    # Get the absolute path of the root before we start jumping around.
    if not os.path.isdir(path):
        try:
            mkdirp(path)
        except OSError as e:
            raise MirrorError("Cannot create directory '%s':" % path, str(e))
    mirror_cache = spack.caches.MirrorCache(path, skip_unstable_versions=skip_unstable_versions)
    mirror_stats = MirrorStats()
    return mirror_cache, mirror_stats


def add(mirror: Mirror, scope=None):
    """Add a named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml_dict()

    if mirror.name in mirrors:
        tty.die("Mirror with name {} already exists.".format(mirror.name))

    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (mirror.name, mirror.to_dict()))
    mirrors = syaml_dict(items)
    spack.config.set("mirrors", mirrors, scope=scope)


def remove(name, scope):
    """Remove the named mirror in the given scope"""
    mirrors = spack.config.get("mirrors", scope=scope)
    if not mirrors:
        mirrors = syaml_dict()

    if name not in mirrors:
        tty.die("No mirror with name %s" % name)

    old_value = mirrors.pop(name)
    spack.config.set("mirrors", mirrors, scope=scope)

    debug_msg_url = "url %s"
    debug_msg = ["Removed mirror %s with"]
    values = [name]

    try:
        fetch_value = old_value["fetch"]
        push_value = old_value["push"]

        debug_msg.extend(("fetch", debug_msg_url, "and push", debug_msg_url))
        values.extend((fetch_value, push_value))
    except TypeError:
        debug_msg.append(debug_msg_url)
        values.append(old_value)

    tty.debug(" ".join(debug_msg) % tuple(values))
    tty.msg("Removed mirror %s." % name)


class MirrorStats(object):
    def __init__(self):
        self.present = {}
        self.new = {}
        self.errors = set()

        self.current_spec = None
        self.added_resources = set()
        self.existing_resources = set()

    def next_spec(self, spec):
        self._tally_current_spec()
        self.current_spec = spec

    def _tally_current_spec(self):
        if self.current_spec:
            if self.added_resources:
                self.new[self.current_spec] = len(self.added_resources)
            if self.existing_resources:
                self.present[self.current_spec] = len(self.existing_resources)
            self.added_resources = set()
            self.existing_resources = set()
        self.current_spec = None

    def stats(self):
        self._tally_current_spec()
        return list(self.present), list(self.new), list(self.errors)

    def already_existed(self, resource):
        # If an error occurred after caching a subset of a spec's
        # resources, a secondary attempt may consider them already added
        if resource not in self.added_resources:
            self.existing_resources.add(resource)

    def added(self, resource):
        self.added_resources.add(resource)

    def error(self):
        self.errors.add(self.current_spec)


def create_mirror_from_package_object(pkg_obj, mirror_cache, mirror_stats):
    """Add a single package object to a mirror.

    The package object is only required to have an associated spec
    with a concrete version.

    Args:
        pkg_obj (spack.package_base.PackageBase): package object with to be added.
        mirror_cache (spack.caches.MirrorCache): mirror where to add the spec.
        mirror_stats (spack.mirror.MirrorStats): statistics on the current mirror

    Return:
        True if the spec was added successfully, False otherwise
    """
    tty.msg("Adding package {} to mirror".format(pkg_obj.spec.format("{name}{@version}")))
    num_retries = 3
    while num_retries > 0:
        try:
            with pkg_obj.stage as pkg_stage:
                pkg_stage.cache_mirror(mirror_cache, mirror_stats)
                for patch in pkg_obj.all_patches():
                    if patch.stage:
                        patch.stage.cache_mirror(mirror_cache, mirror_stats)
                    patch.clean()
            exception = None
            break
        except Exception as e:
            exc_tuple = sys.exc_info()
            exception = e
        num_retries -= 1
    if exception:
        if spack.config.get("config:debug"):
            traceback.print_exception(file=sys.stderr, *exc_tuple)
        else:
            tty.warn(
                "Error while fetching %s" % pkg_obj.spec.cformat("{name}{@version}"),
                getattr(exception, "message", exception),
            )
        mirror_stats.error()
        return False
    return True


def require_mirror_name(mirror_name):
    """Find a mirror by name and raise if it does not exist"""
    mirror = spack.mirror.MirrorCollection().get(mirror_name)
    if not mirror:
        raise ValueError('no mirror named "{0}"'.format(mirror_name))
    return mirror


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
