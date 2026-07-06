# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Utility functions for parsing, formatting, and manipulating URLs.
"""

import itertools
import os
import posixpath
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional, Set, Tuple
from urllib.parse import urlsplit, urlunsplit

from spack.util.path import sanitize_filename

# Archive extensions allowed in Spack
PREFIX_EXTENSIONS = ("tar", "TAR")
EXTENSIONS = ("gz", "bz2", "xz", "Z")
NO_TAR_EXTENSIONS = ("zip", "tgz", "tbz2", "tbz", "txz", "whl")

# Add PREFIX_EXTENSIONS and EXTENSIONS last so that .tar.gz is matched *before* .tar or .gz
ALLOWED_ARCHIVE_TYPES = (
    tuple(".".join(ext) for ext in itertools.product(PREFIX_EXTENSIONS, EXTENSIONS))
    + PREFIX_EXTENSIONS
    + EXTENSIONS
    + NO_TAR_EXTENSIONS
)
CONTRACTION_MAP = {"tgz": "tar.gz", "txz": "tar.xz", "tbz": "tar.bz2", "tbz2": "tar.bz2"}


def validate_scheme(scheme):
    """Returns true if the URL scheme is generally known to Spack. This function
    helps mostly in validation of paths vs urls, as Windows paths such as
    C:/x/y/z (with backward not forward slash) may parse as a URL with scheme
    C and path /x/y/z."""
    return scheme in ("file", "http", "https", "ftp", "s3", "gs", "ssh", "git", "oci")


def local_file_path(url):
    """Get a local file path from a url.

    If url is a ``file://`` URL, return the absolute path to the local
    file or directory referenced by it.  Otherwise, return None.
    """
    if isinstance(url, str):
        url = urllib.parse.urlparse(url)

    if url.scheme == "file":
        return urllib.request.url2pathname(url.path)

    return None


def path_to_file_url(path):
    return Path(path).absolute().as_uri()


def file_url_string_to_path(url):
    return urllib.request.url2pathname(urllib.parse.urlparse(url).path)


def is_path_instead_of_url(path_or_url):
    """Historically some config files and spack commands used paths
    where urls should be used. This utility can be used to validate
    and promote paths to urls."""
    return not validate_scheme(urllib.parse.urlparse(path_or_url).scheme)


def format(parsed_url):
    """Format a URL string

    Returns a canonicalized format of the given URL as a string.
    """
    if isinstance(parsed_url, str):
        parsed_url = urllib.parse.urlparse(parsed_url)

    return parsed_url.geturl()


def join(base: str, *components: str, resolve_href: bool = False, **kwargs) -> str:
    """Convenience wrapper around :func:`urllib.parse.urljoin`, with a few differences:

    1. By default ``resolve_href=False``, which makes the function like :func:`os.path.join`.
       For example ``https://example.com/a/b + c/d = https://example.com/a/b/c/d``. If
       ``resolve_href=True``, the behavior is how a browser would resolve the URL:
       ``https://example.com/a/c/d``.
    2. ``s3://``, ``gs://``, ``oci://`` URLs are joined like ``http://`` URLs.
    3. It accepts multiple components for convenience. Note that ``components[1:]`` are treated as
       literal path components and appended to ``components[0]`` separated by slashes."""
    # Ensure a trailing slash in the path component of the base URL to get os.path.join-like
    # behavior instead of web browser behavior.
    if not resolve_href:
        parsed = urllib.parse.urlparse(base)
        if not parsed.path.endswith("/"):
            base = parsed._replace(path=f"{parsed.path}/").geturl()
    old_netloc = urllib.parse.uses_netloc
    old_relative = urllib.parse.uses_relative
    try:
        # NOTE: we temporarily modify urllib internals so s3 and gs schemes are treated like http.
        # This is non-portable, and may be forward incompatible with future cpython versions.
        urllib.parse.uses_netloc = [*old_netloc, "s3", "gs", "oci", "oci+http"]  # type: ignore
        urllib.parse.uses_relative = [*old_relative, "s3", "gs", "oci", "oci+http"]  # type: ignore
        return urllib.parse.urljoin(base, "/".join(components), **kwargs)
    finally:
        urllib.parse.uses_netloc = old_netloc  # type: ignore
        urllib.parse.uses_relative = old_relative  # type: ignore


def default_download_filename(url: str) -> str:
    """This method computes a default file name for a given URL.
    Note that it makes no request, so this is not the same as the
    option curl -O, which uses the remote file name from the response
    header."""
    parsed_url = urllib.parse.urlparse(url)
    # Only use the last path component + params + query + fragment
    name = urllib.parse.urlunparse(
        parsed_url._replace(scheme="", netloc="", path=posixpath.basename(parsed_url.path))
    )
    valid_name = sanitize_filename(name)

    # Don't download to hidden files please
    if valid_name[0] == ".":
        valid_name = "_" + valid_name[1:]

    return valid_name


def parse_link_rel_next(link_value: str) -> Optional[str]:
    """Return the next link from a Link header value, if any."""

    # Relaxed version of RFC5988
    uri = re.compile(r"\s*<([^>]+)>\s*")
    param_key = r"[^;=\s]+"
    quoted_string = r"\"([^\"]+)\""
    unquoted_param_value = r"([^;,\s]+)"
    param = re.compile(rf";\s*({param_key})\s*=\s*(?:{quoted_string}|{unquoted_param_value})\s*")

    data = link_value

    # Parse a list of <url>; key=value; key=value, <url>; key=value; key=value, ... links.
    while True:
        uri_match = re.match(uri, data)
        if not uri_match:
            break
        uri_reference = uri_match.group(1)
        data = data[uri_match.end() :]

        # Parse parameter list
        while True:
            param_match = re.match(param, data)
            if not param_match:
                break
            key, quoted_value, unquoted_value = param_match.groups()
            value = quoted_value or unquoted_value
            data = data[param_match.end() :]

            if key == "rel" and value == "next":
                return uri_reference

        if not data.startswith(","):
            break

        data = data[1:]

    return None


# ==============================================================================
# Archive extension functions (originally from spack.llnl.url)
# ==============================================================================


def find_list_urls(url: str) -> Set[str]:
    r"""Find good list URLs for the supplied URL.

    By default, returns the dirname of the archive path.

    Provides special treatment for the following websites, which have a
    unique list URL different from the dirname of the download URL:

    =========  =======================================================
    GitHub     ``https://github.com/<repo>/<name>/releases``
    GitLab     ``https://gitlab.\*/<repo>/<name>/tags``
    BitBucket  ``https://bitbucket.org/<repo>/<name>/downloads/?tab=tags``
    CRAN       ``https://\*.r-project.org/src/contrib/Archive/<name>``
    PyPI       ``https://pypi.org/simple/<name>/``
    LuaRocks   ``https://luarocks.org/modules/<repo>/<name>``
    =========  =======================================================

    Note: this function is called by ``spack versions``, ``spack checksum``,
    and ``spack create``, but not by ``spack fetch`` or ``spack install``.

    Parameters:
        url (str): The download URL for the package

    Returns:
        set: One or more list URLs for the package
    """

    url_types = [
        # GitHub
        # e.g. https://github.com/llnl/callpath/archive/v1.0.1.tar.gz
        (r"(.*github\.com/[^/]+/[^/]+)", lambda m: m.group(1) + "/releases"),
        # GitLab API endpoint
        # e.g. https://gitlab.dkrz.de/api/v4/projects/k202009%2Flibaec/repository/archive.tar.gz?sha=v1.0.2
        (
            r"(.*gitlab[^/]+)/api/v4/projects/([^/]+)%2F([^/]+)",
            lambda m: m.group(1) + "/" + m.group(2) + "/" + m.group(3) + "/tags",
        ),
        # GitLab non-API endpoint
        # e.g. https://gitlab.dkrz.de/k202009/libaec/uploads/631e85bcf877c2dcaca9b2e6d6526339/libaec-1.0.0.tar.gz
        (r"(.*gitlab[^/]+/(?!api/v4/projects)[^/]+/[^/]+)", lambda m: m.group(1) + "/tags"),
        # BitBucket
        # e.g. https://bitbucket.org/eigen/eigen/get/3.3.3.tar.bz2
        (r"(.*bitbucket.org/[^/]+/[^/]+)", lambda m: m.group(1) + "/downloads/?tab=tags"),
        # CRAN
        # e.g. https://cran.r-project.org/src/contrib/Rcpp_0.12.9.tar.gz
        # e.g. https://cloud.r-project.org/src/contrib/rgl_0.98.1.tar.gz
        (
            r"(.*\.r-project\.org/src/contrib)/([^_]+)",
            lambda m: m.group(1) + "/Archive/" + m.group(2),
        ),
        # PyPI
        # e.g. https://pypi.io/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://www.pypi.io/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://pypi.org/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://pypi.python.org/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://files.pythonhosted.org/packages/source/n/numpy/numpy-1.19.4.zip
        # e.g. https://pypi.io/packages/py2.py3/o/opencensus-context/opencensus_context-0.1.1-py2.py3-none-any.whl
        (
            r"(?:pypi|pythonhosted)[^/]+/packages/[^/]+/./([^/]+)",
            lambda m: "https://pypi.org/simple/" + m.group(1) + "/",
        ),
        # LuaRocks
        # e.g. https://luarocks.org/manifests/gvvaughan/lpeg-1.0.2-1.src.rock
        # e.g. https://luarocks.org/manifests/openresty/lua-cjson-2.1.0-1.src.rock
        (
            r"luarocks[^/]+/(?:modules|manifests)/(?P<org>[^/]+)/"
            + r"(?P<name>.+?)-[0-9.-]*\.src\.rock",
            lambda m: (
                "https://luarocks.org/modules/" + m.group("org") + "/" + m.group("name") + "/"
            ),
        ),
    ]

    list_urls = {os.path.dirname(url)}

    for pattern, fun in url_types:
        match = re.search(pattern, url)
        if match:
            list_urls.add(fun(match))

    return list_urls


def strip_query_and_fragment(url: str) -> Tuple[str, str]:
    """Strips query and fragment from a url, then returns the base url and the suffix.

    Args:
        url: URL to be stripped

    Raises:
        ValueError: when there is any error parsing the URL
    """
    components = urlsplit(url)
    stripped = components[:3] + (None, None)

    query, frag = components[3:5]
    suffix = ""
    if query:
        suffix += "?" + query
    if frag:
        suffix += "#" + frag

    return urlunsplit(stripped), suffix


SOURCEFORGE_RE = re.compile(r"(.*(?:sourceforge\.net|sf\.net)/.*)(/download)$")


def split_url_on_sourceforge_suffix(url: str) -> Tuple[str, ...]:
    """If the input is a sourceforge URL, returns base URL and ``/download`` suffix. Otherwise,
    returns the input URL and an empty string.
    """
    match = SOURCEFORGE_RE.search(url)
    if match is not None:
        return match.groups()
    return url, ""


def has_extension(path_or_url: str, ext: str) -> bool:
    """Returns true if the extension in input is present in path, false otherwise."""
    prefix, _ = split_url_on_sourceforge_suffix(path_or_url)
    if not ext.startswith(r"\."):
        ext = rf"\.{ext}$"

    if re.search(ext, prefix):
        return True
    return False


def extension_from_path(path_or_url: Optional[str]) -> Optional[str]:
    """Tries to match an allowed archive extension to the input. Returns the first match,
    or None if no match was found.

    Raises:
        ValueError: if the input is None
    """
    if path_or_url is None:
        raise ValueError("Can't call extension() on None")

    for t in ALLOWED_ARCHIVE_TYPES:
        if has_extension(path_or_url, t):
            return t
    return None


def remove_extension(path_or_url: str, *, extension: str) -> str:
    """Returns the input with the extension removed"""
    suffix = rf"\.{extension}$"
    return re.sub(suffix, "", path_or_url)


def check_and_remove_ext(path: str, *, extension: str) -> str:
    """Returns the input path with the extension removed, if the extension is present in path.
    Otherwise, returns the input unchanged.
    """
    if not has_extension(path, extension):
        return path
    path, _ = split_url_on_sourceforge_suffix(path)
    return remove_extension(path, extension=extension)


def strip_extension(path_or_url: str, *, extension: Optional[str] = None) -> str:
    """If a path contains the extension in input, returns the path stripped of the extension.
    Otherwise, returns the input path.

    If extension is None, attempts to strip any allowed extension from path.
    """
    if extension is None:
        for t in ALLOWED_ARCHIVE_TYPES:
            if has_extension(path_or_url, ext=t):
                extension = t
                break
        else:
            return path_or_url

    return check_and_remove_ext(path_or_url, extension=extension)


def split_url_extension(url: str) -> Tuple[str, ...]:
    """Some URLs have a query string, e.g.:

    1. ``https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true``
    2. ``http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin.tar.gz``
    3. ``https://gitlab.kitware.com/vtk/vtk/repository/archive.tar.bz2?ref=v7.0.0``

    In (1), the query string needs to be stripped to get at the
    extension, but in (2) & (3), the filename is IN a single final query
    argument.

    This strips the URL into three pieces: ``prefix``, ``ext``, and ``suffix``.
    The suffix contains anything that was stripped off the URL to
    get at the file extension.  In (1), it will be ``'?raw=true'``, but
    in (2), it will be empty. In (3) the suffix is a parameter that follows
    after the file extension, e.g.:

    1. ``('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7', '.tgz', '?raw=true')``
    2. ``('http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin', '.tar.gz', None)``
    3. ``('https://gitlab.kitware.com/vtk/vtk/repository/archive', '.tar.bz2', '?ref=v7.0.0')``
    """  # noqa: E501
    # Strip off sourceforge download suffix.
    # e.g. https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download
    prefix, suffix = split_url_on_sourceforge_suffix(url)

    ext = extension_from_path(prefix)
    if ext is not None:
        prefix = strip_extension(prefix)
        return prefix, ext, suffix

    try:
        prefix, suf = strip_query_and_fragment(prefix)
    except ValueError:
        # FIXME: tty.debug("Got error parsing path %s" % path)
        # Ignore URL parse errors here
        return url, ""

    ext = extension_from_path(prefix)
    prefix = strip_extension(prefix)
    suffix = suf + suffix
    if ext is None:
        ext = ""

    return prefix, ext, suffix


def strip_version_suffixes(path_or_url: str) -> str:
    """Some tarballs contain extraneous information after the version:

    * ``bowtie2-2.2.5-source``
    * ``libevent-2.0.21-stable``
    * ``cuda_8.0.44_linux.run``

    These strings are not part of the version number and should be ignored.
    This function strips those suffixes off and returns the remaining string.
    The goal is that the version is always the last thing in ``path``:

    * ``bowtie2-2.2.5``
    * ``libevent-2.0.21``
    * ``cuda_8.0.44``

    Args:
        path_or_url: The filename or URL for the package

    Returns:
        The ``path`` with any extraneous suffixes removed
    """
    # NOTE: This could be done with complicated regexes in parse_version_offset
    # NOTE: The problem is that we would have to add these regexes to the end
    # NOTE: of every single version regex. Easier to just strip them off
    # NOTE: permanently

    suffix_regexes = [
        # Download type
        r"[Ii]nstall",
        r"all",
        r"code",
        r"[Ss]ources?",
        r"file",
        r"full",
        r"single",
        r"with[a-zA-Z_-]+",
        r"rock",
        r"src(_0)?",
        r"public",
        r"bin",
        r"binary",
        r"run",
        r"[Uu]niversal",
        r"jar",
        r"complete",
        r"dynamic",
        r"oss",
        r"gem",
        r"tar",
        r"sh",
        # Download version
        r"release",
        r"bin",
        r"stable",
        r"[Ff]inal",
        r"rel",
        r"orig",
        r"dist",
        r"\+",
        # License
        r"gpl",
        # Arch
        # Needs to come before and after OS, appears in both orders
        r"ia32",
        r"intel",
        r"amd64",
        r"linux64",
        r"x64",
        r"64bit",
        r"x86[_-]64",
        r"i586_64",
        r"x86",
        r"i[36]86",
        r"ppc64(le)?",
        r"armv?(7l|6l|64)",
        # Other
        r"cpp",
        r"gtk",
        r"incubating",
        # OS
        r"[Ll]inux(_64)?",
        r"LINUX",
        r"[Uu]ni?x",
        r"[Ss]un[Oo][Ss]",
        r"[Mm]ac[Oo][Ss][Xx]?",
        r"[Oo][Ss][Xx]",
        r"[Dd]arwin(64)?",
        r"[Aa]pple",
        r"[Ww]indows",
        r"[Ww]in(64|32)?",
        r"[Cc]ygwin(64|32)?",
        r"[Mm]ingw",
        r"centos",
        # Arch
        # Needs to come before and after OS, appears in both orders
        r"ia32",
        r"intel",
        r"amd64",
        r"linux64",
        r"x64",
        r"64bit",
        r"x86[_-]64",
        r"i586_64",
        r"x86",
        r"i[36]86",
        r"ppc64(le)?",
        r"armv?(7l|6l|64)?",
        # PyPI wheels
        r"-(?:py|cp)[23].*",
    ]

    for regex in suffix_regexes:
        # Remove the suffix from the end of the path
        # This may be done multiple times
        path_or_url = re.sub(r"[._-]?" + regex + "$", "", path_or_url)

    return path_or_url


def expand_contracted_extension(extension: str) -> str:
    """Returns the expanded version of a known contracted extension.

    This function maps extensions like ``.tgz`` to ``.tar.gz``. On unknown extensions,
    return the input unmodified.
    """
    extension = extension.strip(".")
    return CONTRACTION_MAP.get(extension, extension)


def expand_contracted_extension_in_path(
    path_or_url: str, *, extension: Optional[str] = None
) -> str:
    """Returns the input path or URL with any contraction extension expanded.

    Args:
        path_or_url: path or URL to be expanded
        extension: if specified, only attempt to expand that extension
    """
    extension = extension or extension_from_path(path_or_url)
    if extension is None:
        return path_or_url

    expanded = expand_contracted_extension(extension)
    if expanded != extension:
        return re.sub(rf"{extension}", rf"{expanded}", path_or_url)
    return path_or_url


def compression_ext_from_compressed_archive(extension: str) -> Optional[str]:
    """Returns compression extension for a compressed archive"""
    extension = expand_contracted_extension(extension)
    for ext in EXTENSIONS:
        if ext in extension:
            return ext
    return None


def strip_compression_extension(path_or_url: str, ext: Optional[str] = None) -> str:
    """Strips the compression extension from the input, and returns it. For instance,
    ``"foo.tgz"`` becomes ``"foo.tar"``.

    If no extension is given, try a default list of extensions.

    Args:
        path_or_url: input to be stripped
        ext: if given, extension to be stripped
    """
    if not extension_from_path(path_or_url):
        return path_or_url

    expanded_path = expand_contracted_extension_in_path(path_or_url)
    candidates = [ext] if ext is not None else EXTENSIONS
    for current_extension in candidates:
        modified_path = check_and_remove_ext(expanded_path, extension=current_extension)
        if modified_path != expanded_path:
            return modified_path
    return expanded_path


def allowed_archive(path_or_url: str) -> bool:
    """Returns true if the input is a valid archive, False otherwise."""
    return (
        False if not path_or_url else any(path_or_url.endswith(t) for t in ALLOWED_ARCHIVE_TYPES)
    )


def determine_url_file_extension(path: str) -> str:
    """This returns the type of archive a URL refers to.  This is
    sometimes confusing because of URLs like:

    (1) ``https://github.com/petdance/ack/tarball/1.93_02``

    Where the URL doesn't actually contain the filename.  We need
    to know what type it is so that we can appropriately name files
    in mirrors.
    """
    match = re.search(r"github.com/.+/(zip|tar)ball/", path)
    if match:
        if match.group(1) == "zip":
            return "zip"
        elif match.group(1) == "tar":
            return "tar.gz"

    prefix, ext, suffix = split_url_extension(path)
    return ext
