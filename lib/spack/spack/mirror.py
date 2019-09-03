# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
import re
import sys
import os
import os.path
import operator

import six

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.config
import spack.error
import spack.url as url
import spack.fetch_strategy as fs
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
from spack.spec import Spec
from spack.version import VersionList
from spack.util.compression import allowed_archive
from spack.util.url import parse as url_parse
from spack.util.spack_yaml import syaml_dict


def _display_mirror_entry(size, name, url, type_=None):
    if type_:
        type_ = "".join((" (", type_, ")"))
    else:
        type_ = ""

    print("%-*s%s%s" % (size + 4, name, url, type_))

class Mirror(object):
    """Represents a named location for storing source tarballs and binary
    packages.

    Mirrors have a fetch_url that indicate where and how artifacts are fetched
    from them, and a push_url that indicate where and how artifacts are pushed
    to them.  These two URLs are usually the same.
    """

    def __init__(self, fetch_url, push_url=None, name=None):
        self._fetch_url = fetch_url
        self._push_url = push_url
        self._name = name

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(), stream)

    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return Mirror.from_dict(data, name)
        except MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    @staticmethod
    def from_json(stream, name=None):
        d = sjson.load(stream)
        return Mirror.from_dict(d, name)

    def to_dict(self):
        if self._push_url is None:
            return self._fetch_url
        else:
            return syaml_dict([
                ('fetch', self._fetch_url),
                ('push', self._push_url)])

    @staticmethod
    def from_dict(d, name=None):
        if isinstance(d, six.string_types):
            return Mirror(d, name=name)
        else:
            return Mirror(d['fetch'], d['push'], name)

    def display(self, max_len=0):
        if self._push_url is None:
            _display_mirror_entry(max_len, self._name, self._fetch_url)
        else:
            _display_mirror_entry(
                    max_len, self._name, self._fetch_url, "fetch")
            _display_mirror_entry(
                    max_len, self._name, self._push_url, "push")

    def __str__(self):
        name = self._name
        if name is None:
            name = ''
        else:
            name = ' "%s"' % name

        if self._push_url is None:
            return "[Mirror%s (%s)]" % (name, self._fetch_url)

        return "[Mirror%s (fetch: %s, push: %s)]" % (
                name, self._fetch_url, self._push_url)

    def __repr__(self):
        return ''.join((
            'Mirror(',
            ', '.join(
                '%s=%s' % (k, repr(v))
                for k, v in (
                    ('fetch_url', self._fetch_url),
                    ('push_url', self._push_url),
                    ('name', self._name))
                if k == 'fetch_url' or v),
            ')'
        ))

    @property
    def name(self):
        return self._name or "<unnamed>"

    @property
    def fetch_url(self):
        return self._fetch_url

    @fetch_url.setter
    def fetch_url(self, url):
        self._fetch_url = url
        self._normalize()

    @property
    def push_url(self):
        if self._push_url is None:
            return self._fetch_url
        return self._push_url

    @push_url.setter
    def push_url(self, url):
        self._push_url = url
        self._normalize()

    def _normalize(self):
        if self._push_url is not None and self._push_url == self._fetch_url:
            self._push_url = None


class MirrorCollection(Mapping):
    """A mapping of mirror names to mirrors."""

    def __init__(self, mirrors=None, scope=None):
        self._mirrors = dict(
            (name, Mirror.from_dict(mirror, name))
            for name, mirror in (
                mirrors.items() if mirrors is not None else
                spack.config.get('mirrors', scope=scope).items()))

    def to_json(self, stream=None):
        return sjson.dump(self.to_dict(True), stream)

    def to_yaml(self, stream=None):
        return syaml.dump(self.to_dict(True), stream)

    @staticmethod
    def from_yaml(stream, name=None):
        try:
            data = syaml.load(stream)
            return MirrorCollection(data)
        except MarkedYAMLError as e:
            raise syaml.SpackYAMLError("error parsing YAML spec:", str(e))

    @staticmethod
    def from_json(stream, name=None):
        d = sjson.load(stream)
        return MirrorCollection(d)

    def to_dict(self, recursive=False):
        return syaml_dict(sorted(
            (
                (k, (v.to_dict() if recursive else v))
                for (k, v) in self._mirrors.items()
            ), key=operator.itemgetter(0)
        ))

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


def mirror_archive_filename(spec, fetcher, resource_id=None):
    """Get the name of the spec's archive in the mirror."""
    if not spec.version.concrete:
        raise ValueError("mirror.path requires spec with concrete version.")

    if isinstance(fetcher, fs.URLFetchStrategy):
        if fetcher.expand_archive:
            # If we fetch with a URLFetchStrategy, use URL's archive type
            ext = url.determine_url_file_extension(fetcher.url)

            # If the filename does not end with a normal suffix,
            # see if the package explicitly declares the extension
            if not ext:
                ext = spec.package.versions[spec.package.version].get(
                    'extension', None)

            if ext:
                # Remove any leading dots
                ext = ext.lstrip('.')

            if not ext:
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
        ext = 'tar.gz'

    if resource_id:
        filename = "%s-%s" % (resource_id, spec.version) + ".%s" % ext
    else:
        filename = "%s-%s" % (spec.package.name, spec.version) + ".%s" % ext

    return filename


def mirror_archive_path(spec, fetcher, resource_id=None):
    """Get the relative path to the spec's archive within a mirror."""
    return os.path.join(
        spec.name, mirror_archive_filename(spec, fetcher, resource_id))


def get_matching_versions(specs, **kwargs):
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

        pkg_versions = kwargs.get('num_versions', 1)

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
            if spec.concrete or v.satisfies(spec.versions):
                s = Spec(pkg.name)
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


def suggest_archive_basename(resource):
    """Return a tentative basename for an archive.

    Raises:
        RuntimeError: if the name is not an allowed archive type.
    """
    basename = os.path.basename(resource.fetcher.url)
    if not allowed_archive(basename):
        raise RuntimeError("%s is not an allowed archive tye" % basename)
    return basename


def create(path, specs, **kwargs):
    """Create a directory to be used as a spack mirror, and fill it with
    package archives.

    Arguments:
        path: Path to create a mirror directory hierarchy in.
        specs: Any package versions matching these specs will be added \
            to the mirror.

    Keyword args:
        num_versions: Max number of versions to fetch per spec, \
            (default is 1 each spec)

    Return Value:
        Returns a tuple of lists: (present, mirrored, error)

        * present:  Package specs that were already present.
        * mirrored: Package specs that were successfully mirrored.
        * error:    Package specs that failed to mirror due to some error.

    This routine iterates through all known package versions, and
    it creates specs for those versions.  If the version satisfies any spec
    in the specs list, it is downloaded and added to the mirror.
    """
    parsed = url_parse(path)
    is_file_scheme = (parsed.scheme == 'file')

    # Make sure nothing is in the way.
    if is_file_scheme and os.path.isfile(parsed.path):
        raise MirrorError("%s already exists and is a file." % parsed.path)

    # automatically spec-ify anything in the specs array.
    specs = [s if isinstance(s, Spec) else Spec(s) for s in specs]

    # Get concrete specs for each matching version of these specs.
    version_specs = get_matching_versions(
        specs, num_versions=kwargs.get('num_versions', 1))
    for s in version_specs:
        s.concretize()

    # Get the absolute path of the root before we start jumping around.
    mirror_root = parsed.path
    if is_file_scheme and not os.path.isdir(mirror_root):
        try:
            mkdirp(mirror_root)
        except OSError as e:
            raise MirrorError(
                "Cannot create directory '%s':" % mirror_root, str(e))

    # Things to keep track of while parsing specs.
    categories = {
        'present': [],
        'mirrored': [],
        'error': []
    }

    mirror_cache = spack.caches.MirrorCache(parsed)
    try:
        spack.caches.mirror_cache = mirror_cache
        # Iterate through packages and download all safe tarballs for each
        for spec in version_specs:
            add_single_spec(spec, parsed, categories, **kwargs)
    finally:
        spack.caches.mirror_cache = None

    categories['mirrored'] = list(mirror_cache.new_resources)
    categories['present'] = list(mirror_cache.existing_resources)

    return categories['present'], categories['mirrored'], categories['error']


def add_single_spec(spec, mirror_root, categories, **kwargs):
    tty.msg("Adding package {pkg} to mirror".format(
        pkg=spec.format("{name}{@version}")
    ))
    try:
        spec.package.do_fetch()
        spec.package.do_clean()

    except Exception as e:
        tty.debug(e)
        if spack.config.get('config:debug'):
            sys.excepthook(*sys.exc_info())
        else:
            tty.warn(
                "Error while fetching %s" % spec.cformat('{name}{@version}'),
                e.message)
        categories['error'].append(spec)


class MirrorError(spack.error.SpackError):
    """Superclass of all mirror-creation related errors."""

    def __init__(self, msg, long_msg=None):
        super(MirrorError, self).__init__(msg, long_msg)
