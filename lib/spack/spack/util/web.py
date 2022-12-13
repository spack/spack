# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import codecs
import errno
import multiprocessing.pool
import os
import os.path
import re
import shutil
import ssl
import sys
import traceback
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.request import Request, urlopen

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, rename, working_dir

import spack
import spack.config
import spack.error
import spack.url
import spack.util.crypto
import spack.util.gcs as gcs_util
import spack.util.s3 as s3_util
import spack.util.url as url_util
from spack.util.compression import ALLOWED_ARCHIVE_TYPES
from spack.util.executable import CommandNotFoundError, which
from spack.util.path import convert_to_posix_path

#: User-Agent used in Request objects
SPACK_USER_AGENT = "Spackbot/{0}".format(spack.spack_version)


# Also, HTMLParseError is deprecated and never raised.
class HTMLParseError(Exception):
    pass


class LinkParser(HTMLParser):
    """This parser just takes an HTML page and strips out the hrefs on the
    links.  Good enough for a really simple spider."""

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href":
                    self.links.append(val)


def uses_ssl(parsed_url):
    if parsed_url.scheme == "https":
        return True

    if parsed_url.scheme == "s3":
        endpoint_url = os.environ.get("S3_ENDPOINT_URL")
        if not endpoint_url:
            return True

        if url_util.parse(endpoint_url, scheme="https").scheme == "https":
            return True

    elif parsed_url.scheme == "gs":
        tty.debug("(uses_ssl) GCS Blob is https")
        return True

    return False


def read_from_url(url, accept_content_type=None):
    url = url_util.parse(url)
    context = None

    # Timeout in seconds for web requests
    timeout = spack.config.get("config:connect_timeout", 10)

    # Don't even bother with a context unless the URL scheme is one that uses
    # SSL certs.
    if uses_ssl(url):
        if spack.config.get("config:verify_ssl"):
            # User wants SSL verification, and it *can* be provided.
            context = ssl.create_default_context()
        else:
            # User has explicitly indicated that they do not want SSL
            # verification.
            context = ssl._create_unverified_context()

    url_scheme = url.scheme
    url = url_util.format(url)
    if sys.platform == "win32" and url_scheme == "file":
        url = convert_to_posix_path(url)
    req = Request(url, headers={"User-Agent": SPACK_USER_AGENT})

    content_type = None
    is_web_url = url_scheme in ("http", "https")
    if accept_content_type and is_web_url:
        # Make a HEAD request first to check the content type.  This lets
        # us ignore tarballs and gigantic files.
        # It would be nice to do this with the HTTP Accept header to avoid
        # one round-trip.  However, most servers seem to ignore the header
        # if you ask for a tarball with Accept: text/html.
        req.get_method = lambda: "HEAD"
        resp = _urlopen(req, timeout=timeout, context=context)

        content_type = get_header(resp.headers, "Content-type")

    # Do the real GET request when we know it's just HTML.
    req.get_method = lambda: "GET"

    try:
        response = _urlopen(req, timeout=timeout, context=context)
    except URLError as err:
        raise SpackWebError("Download failed: {ERROR}".format(ERROR=str(err)))

    if accept_content_type and not is_web_url:
        content_type = get_header(response.headers, "Content-type")

    reject_content_type = accept_content_type and (
        content_type is None or not content_type.startswith(accept_content_type)
    )

    if reject_content_type:
        tty.debug(
            "ignoring page {0}{1}{2}".format(
                url, " with content type " if content_type is not None else "", content_type or ""
            )
        )

        return None, None, None

    return response.geturl(), response.headers, response


def push_to_url(local_file_path, remote_path, keep_original=True, extra_args=None):
    if sys.platform == "win32":
        if remote_path[1] == ":":
            remote_path = "file://" + remote_path
    remote_url = url_util.parse(remote_path)

    remote_file_path = url_util.local_file_path(remote_url)
    if remote_file_path is not None:
        mkdirp(os.path.dirname(remote_file_path))
        if keep_original:
            shutil.copy(local_file_path, remote_file_path)
        else:
            try:
                rename(local_file_path, remote_file_path)
            except OSError as e:
                if e.errno == errno.EXDEV:
                    # NOTE(opadron): The above move failed because it crosses
                    # filesystem boundaries.  Copy the file (plus original
                    # metadata), and then delete the original.  This operation
                    # needs to be done in separate steps.
                    shutil.copy2(local_file_path, remote_file_path)
                    os.remove(local_file_path)
                else:
                    raise

    elif remote_url.scheme == "s3":
        if extra_args is None:
            extra_args = {}

        remote_path = remote_url.path
        while remote_path.startswith("/"):
            remote_path = remote_path[1:]

        s3 = s3_util.get_s3_session(remote_url, method="push")
        s3.upload_file(local_file_path, remote_url.netloc, remote_path, ExtraArgs=extra_args)

        if not keep_original:
            os.remove(local_file_path)

    elif remote_url.scheme == "gs":
        gcs = gcs_util.GCSBlob(remote_url)
        gcs.upload_to_blob(local_file_path)
        if not keep_original:
            os.remove(local_file_path)

    else:
        raise NotImplementedError(
            "Unrecognized URL scheme: {SCHEME}".format(SCHEME=remote_url.scheme)
        )


def base_curl_fetch_args(url, timeout=0):
    """Return the basic fetch arguments typically used in calls to curl.

    The arguments include those for ensuring behaviors such as failing on
    errors for codes over 400, printing HTML headers, resolving 3xx redirects,
    status or failure handling, and connection timeouts.

    It also uses the following configuration option to set an additional
    argument as needed:

        * config:connect_timeout (int): connection timeout
        * config:verify_ssl (str): Perform SSL verification

    Arguments:
        url (str): URL whose contents will be fetched
        timeout (int): Connection timeout, which is only used if higher than
            config:connect_timeout

    Returns (list): list of argument strings
    """
    curl_args = [
        "-f",  # fail on >400 errors
        "-D",
        "-",  # "-D -" prints out HTML headers
        "-L",  # resolve 3xx redirects
        url,
    ]
    if not spack.config.get("config:verify_ssl"):
        curl_args.append("-k")

    if sys.stdout.isatty() and tty.msg_enabled():
        curl_args.append("-#")  # status bar when using a tty
    else:
        curl_args.append("-sS")  # show errors if fail

    connect_timeout = spack.config.get("config:connect_timeout", 10)
    if timeout:
        connect_timeout = max(int(connect_timeout), int(timeout))
    if connect_timeout > 0:
        curl_args.extend(["--connect-timeout", str(connect_timeout)])

    return curl_args


def check_curl_code(returncode):
    """Check standard return code failures for provided arguments.

    Arguments:
        returncode (int): curl return code

    Raises FetchError if the curl returncode indicates failure
    """
    if returncode != 0:
        if returncode == 22:
            # This is a 404. Curl will print the error.
            raise FetchError("URL was not found!")

        if returncode == 60:
            # This is a certificate error.  Suggest spack -k
            raise FetchError(
                "Curl was unable to fetch due to invalid certificate. "
                "This is either an attack, or your cluster's SSL "
                "configuration is bad.  If you believe your SSL "
                "configuration is bad, you can try running spack -k, "
                "which will not check SSL certificates."
                "Use this at your own risk."
            )

        raise FetchError("Curl failed with error {0}".format(returncode))


def _curl(curl=None):
    if not curl:
        try:
            curl = which("curl", required=True)
        except CommandNotFoundError as exc:
            tty.error(str(exc))
            raise FetchError("Missing required curl fetch method")
    return curl


def fetch_url_text(url, curl=None, dest_dir="."):
    """Retrieves text-only URL content using the configured fetch method.
    It determines the fetch method from:

        * config:url_fetch_method (str): fetch method to use (e.g., 'curl')

    If the method is `curl`, it also uses the following configuration
    options:

        * config:connect_timeout (int): connection time out
        * config:verify_ssl (str): Perform SSL verification

    Arguments:
        url (str): URL whose contents are to be fetched
        curl (spack.util.executable.Executable or None): (optional) curl
            executable if curl is the configured fetch method
        dest_dir (str): (optional) destination directory for fetched text
            file

    Returns (str or None): path to the fetched file

    Raises FetchError if the curl returncode indicates failure
    """
    if not url:
        raise FetchError("A URL is required to fetch its text")

    tty.debug("Fetching text at {0}".format(url))

    filename = os.path.basename(url)
    path = os.path.join(dest_dir, filename)

    fetch_method = spack.config.get("config:url_fetch_method")
    tty.debug("Using '{0}' to fetch {1} into {2}".format(fetch_method, url, path))
    if fetch_method == "curl":
        curl_exe = _curl(curl)
        if not curl_exe:
            raise FetchError("Missing required fetch method (curl)")

        curl_args = ["-O"]
        curl_args.extend(base_curl_fetch_args(url))

        # Curl automatically downloads file contents as filename
        with working_dir(dest_dir, create=True):
            _ = curl_exe(*curl_args, fail_on_error=False, output=os.devnull)
            check_curl_code(curl_exe.returncode)

        return path

    else:
        try:
            _, _, response = read_from_url(url)

            returncode = response.getcode()
            if returncode and returncode != 200:
                raise FetchError("Urllib failed with error code {0}".format(returncode))

            output = codecs.getreader("utf-8")(response).read()
            if output:
                with working_dir(dest_dir, create=True):
                    with open(filename, "w") as f:
                        f.write(output)

                return path

        except SpackWebError as err:
            raise FetchError("Urllib fetch failed to verify url: {0}".format(str(err)))

    return None


def url_exists(url, curl=None):
    """Determines whether url exists.

    A scheme-specific process is used for Google Storage (`gs`) and Amazon
    Simple Storage Service (`s3`) URLs; otherwise, the configured fetch
    method defined by `config:url_fetch_method` is used.

    If the method is `curl`, it also uses the following configuration option:

        * config:verify_ssl (str): Perform SSL verification

    Otherwise, `urllib` will be used.

    Arguments:
        url (str): URL whose existence is being checked
        curl (spack.util.executable.Executable or None): (optional) curl
            executable if curl is the configured fetch method

    Returns (bool): True if it exists; False otherwise.
    """
    tty.debug("Checking existence of {0}".format(url))
    url_result = url_util.parse(url)

    # Check if a local file
    local_path = url_util.local_file_path(url_result)
    if local_path:
        return os.path.exists(local_path)

    # Check if Amazon Simple Storage Service (S3) .. urllib-based fetch
    if url_result.scheme == "s3":
        # Check for URL-specific connection information
        s3 = s3_util.get_s3_session(url_result, method="fetch")

        try:
            s3.get_object(Bucket=url_result.netloc, Key=url_result.path.lstrip("/"))
            return True
        except s3.ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchKey":
                return False
            raise err

    # Check if Google Storage .. urllib-based fetch
    if url_result.scheme == "gs":
        gcs = gcs_util.GCSBlob(url_result)
        return gcs.exists()

    # Otherwise, use the configured fetch method
    if spack.config.get("config:url_fetch_method") == "curl":
        curl_exe = _curl(curl)
        if not curl_exe:
            return False

        # Telling curl to fetch the first byte (-r 0-0) is supposed to be
        # portable.
        curl_args = ["--stderr", "-", "-s", "-f", "-r", "0-0", url]
        if not spack.config.get("config:verify_ssl"):
            curl_args.append("-k")
        _ = curl_exe(*curl_args, fail_on_error=False, output=os.devnull)
        return curl_exe.returncode == 0

    # If we get here, then the only other fetch method option is urllib.
    # So try to "read" from the URL and assume that *any* non-throwing
    #  response contains the resource represented by the URL.
    try:
        read_from_url(url)
        return True
    except (SpackWebError, URLError) as e:
        tty.debug("Failure reading URL: " + str(e))
        return False


def _debug_print_delete_results(result):
    if "Deleted" in result:
        for d in result["Deleted"]:
            tty.debug("Deleted {0}".format(d["Key"]))
    if "Errors" in result:
        for e in result["Errors"]:
            tty.debug("Failed to delete {0} ({1})".format(e["Key"], e["Message"]))


def remove_url(url, recursive=False):
    url = url_util.parse(url)

    local_path = url_util.local_file_path(url)
    if local_path:
        if recursive:
            shutil.rmtree(local_path)
        else:
            os.remove(local_path)
        return

    if url.scheme == "s3":
        # Try to find a mirror for potential connection information
        s3 = s3_util.get_s3_session(url, method="push")
        bucket = url.netloc
        if recursive:
            # Because list_objects_v2 can only return up to 1000 items
            # at a time, we have to paginate to make sure we get it all
            prefix = url.path.strip("/")
            paginator = s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

            delete_request = {"Objects": []}
            for item in pages.search("Contents"):
                if not item:
                    continue

                delete_request["Objects"].append({"Key": item["Key"]})

                # Make sure we do not try to hit S3 with a list of more
                # than 1000 items
                if len(delete_request["Objects"]) >= 1000:
                    r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                    _debug_print_delete_results(r)
                    delete_request = {"Objects": []}

            # Delete any items that remain
            if len(delete_request["Objects"]):
                r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                _debug_print_delete_results(r)
        else:
            s3.delete_object(Bucket=bucket, Key=url.path.lstrip("/"))
        return

    elif url.scheme == "gs":
        if recursive:
            bucket = gcs_util.GCSBucket(url)
            bucket.destroy(recursive=recursive)
        else:
            blob = gcs_util.GCSBlob(url)
            blob.delete_blob()
        return

    # Don't even try for other URL schemes.


def _iter_s3_contents(contents, prefix):
    for entry in contents:
        key = entry["Key"]

        if not key.startswith("/"):
            key = "/" + key

        key = os.path.relpath(key, prefix)

        if key == ".":
            continue

        yield key


def _list_s3_objects(client, bucket, prefix, num_entries, start_after=None):
    list_args = dict(Bucket=bucket, Prefix=prefix[1:], MaxKeys=num_entries)

    if start_after is not None:
        list_args["StartAfter"] = start_after

    result = client.list_objects_v2(**list_args)

    last_key = None
    if result["IsTruncated"]:
        last_key = result["Contents"][-1]["Key"]

    iter = _iter_s3_contents(result["Contents"], prefix)

    return iter, last_key


def _iter_s3_prefix(client, url, num_entries=1024):
    key = None
    bucket = url.netloc
    prefix = re.sub(r"^/*", "/", url.path)

    while True:
        contents, key = _list_s3_objects(client, bucket, prefix, num_entries, start_after=key)

        for x in contents:
            yield x

        if not key:
            break


def _iter_local_prefix(path):
    for root, _, files in os.walk(path):
        for f in files:
            yield os.path.relpath(os.path.join(root, f), path)


def list_url(url, recursive=False):
    url = url_util.parse(url)

    local_path = url_util.local_file_path(url)
    if local_path:
        if recursive:
            return list(_iter_local_prefix(local_path))
        return [
            subpath
            for subpath in os.listdir(local_path)
            if os.path.isfile(os.path.join(local_path, subpath))
        ]

    if url.scheme == "s3":
        s3 = s3_util.get_s3_session(url, method="fetch")
        if recursive:
            return list(_iter_s3_prefix(s3, url))

        return list(set(key.split("/", 1)[0] for key in _iter_s3_prefix(s3, url)))

    elif url.scheme == "gs":
        gcs = gcs_util.GCSBucket(url)
        return gcs.get_all_blobs(recursive=recursive)


def spider(root_urls, depth=0, concurrency=32):
    """Get web pages from root URLs.

    If depth is specified (e.g., depth=2), then this will also follow
    up to <depth> levels of links from each root.

    Args:
        root_urls (str or list): root urls used as a starting point
            for spidering
        depth (int): level of recursion into links
        concurrency (int): number of simultaneous requests that can be sent

    Returns:
        A dict of pages visited (URL) mapped to their full text and the
        set of visited links.
    """
    # Cache of visited links, meant to be captured by the closure below
    _visited = set()

    def _spider(url, collect_nested):
        """Fetches URL and any pages it links to.

        Prints out a warning only if the root can't be fetched; it ignores
        errors with pages that the root links to.

        Args:
            url (str): url being fetched and searched for links
            collect_nested (bool): whether we want to collect arguments
                for nested spidering on the links found in this url

        Returns:
            A tuple of:
            - pages: dict of pages visited (URL) mapped to their full text.
            - links: set of links encountered while visiting the pages.
            - spider_args: argument for subsequent call to spider
        """
        pages = {}  # dict from page URL -> text content.
        links = set()  # set of all links seen on visited pages.
        subcalls = []

        try:
            response_url, _, response = read_from_url(url, "text/html")
            if not response_url or not response:
                return pages, links, subcalls

            page = codecs.getreader("utf-8")(response).read()
            pages[response_url] = page

            # Parse out the links in the page
            link_parser = LinkParser()
            link_parser.feed(page)

            while link_parser.links:
                raw_link = link_parser.links.pop()
                abs_link = url_util.join(response_url, raw_link.strip(), resolve_href=True)
                links.add(abs_link)

                # Skip stuff that looks like an archive
                if any(raw_link.endswith(s) for s in ALLOWED_ARCHIVE_TYPES):
                    continue

                # Skip already-visited links
                if abs_link in _visited:
                    continue

                # If we're not at max depth, follow links.
                if collect_nested:
                    subcalls.append((abs_link,))
                    _visited.add(abs_link)

        except URLError as e:
            tty.debug(str(e))

            if hasattr(e, "reason") and isinstance(e.reason, ssl.SSLError):
                tty.warn(
                    "Spack was unable to fetch url list due to a "
                    "certificate verification problem. You can try "
                    "running spack -k, which will not check SSL "
                    "certificates. Use this at your own risk."
                )

        except HTMLParseError as e:
            # This error indicates that Python's HTML parser sucks.
            msg = "Got an error parsing HTML."
            tty.warn(msg, url, "HTMLParseError: " + str(e))

        except Exception as e:
            # Other types of errors are completely ignored,
            # except in debug mode
            tty.debug("Error in _spider: %s:%s" % (type(e), str(e)), traceback.format_exc())

        finally:
            tty.debug("SPIDER: [url={0}]".format(url))

        return pages, links, subcalls

    if isinstance(root_urls, str):
        root_urls = [root_urls]

    # Clear the local cache of visited pages before starting the search
    _visited.clear()

    current_depth = 0
    pages, links, spider_args = {}, set(), []

    collect = current_depth < depth
    for root in root_urls:
        root = url_util.parse(root)
        spider_args.append((root, collect))

    tp = multiprocessing.pool.ThreadPool(processes=concurrency)
    try:
        while current_depth <= depth:
            tty.debug(
                "SPIDER: [depth={0}, max_depth={1}, urls={2}]".format(
                    current_depth, depth, len(spider_args)
                )
            )
            results = tp.map(llnl.util.lang.star(_spider), spider_args)
            spider_args = []
            collect = current_depth < depth
            for sub_pages, sub_links, sub_spider_args in results:
                sub_spider_args = [x + (collect,) for x in sub_spider_args]
                pages.update(sub_pages)
                links.update(sub_links)
                spider_args.extend(sub_spider_args)

            current_depth += 1
    finally:
        tp.terminate()
        tp.join()

    return pages, links


def _urlopen(req, *args, **kwargs):
    """Wrapper for compatibility with old versions of Python."""
    url = req
    try:
        url = url.get_full_url()
    except AttributeError:
        pass

    del kwargs["context"]

    opener = urlopen
    if url_util.parse(url).scheme == "s3":
        import spack.s3_handler

        opener = spack.s3_handler.open
    elif url_util.parse(url).scheme == "gs":
        import spack.gcs_handler

        opener = spack.gcs_handler.gcs_open

    try:
        return opener(req, *args, **kwargs)
    except TypeError as err:
        # If the above fails because of 'context', call without 'context'.
        if "context" in kwargs and "context" in str(err):
            del kwargs["context"]
        return opener(req, *args, **kwargs)


def find_versions_of_archive(
    archive_urls, list_url=None, list_depth=0, concurrency=32, reference_package=None
):
    """Scrape web pages for new versions of a tarball. This function prefers URLs in the
    following order: links found on the scraped page that match a url generated by the
    reference package, found and in the archive_urls list, found and derived from those
    in the archive_urls list, and if none are found for a version then the item in the
    archive_urls list is included for the version.

    Args:
        archive_urls (str or list or tuple): URL or sequence of URLs for
            different versions of a package. Typically these are just the
            tarballs from the package file itself. By default, this searches
            the parent directories of archives.
        list_url (str or None): URL for a listing of archives.
            Spack will scrape these pages for download links that look
            like the archive URL.
        list_depth (int): max depth to follow links on list_url pages.
            Defaults to 0.
        concurrency (int): maximum number of concurrent requests
        reference_package (spack.package_base.PackageBase or None): a spack package
            used as a reference for url detection.  Uses the url_for_version
            method on the package to produce reference urls which, if found,
            are preferred.
    """
    if not isinstance(archive_urls, (list, tuple)):
        archive_urls = [archive_urls]

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url is not None:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls |= spack.url.find_list_urls(aurl)

    # Add '/' to the end of the URL. Some web servers require this.
    additional_list_urls = set()
    for lurl in list_urls:
        if not lurl.endswith("/"):
            additional_list_urls.add(lurl + "/")
    list_urls |= additional_list_urls

    # Grab some web pages to scrape.
    pages, links = spider(list_urls, depth=list_depth, concurrency=concurrency)

    # Scrape them for archive URLs
    regexes = []
    for aurl in archive_urls:
        # This creates a regex from the URL with a capture group for
        # the version part of the URL.  The capture group is converted
        # to a generic wildcard, so we can use this to extract things
        # on a page that look like archive URLs.
        url_regex = spack.url.wildcard_version(aurl)

        # We'll be a bit more liberal and just look for the archive
        # part, not the full path.
        url_regex = os.path.basename(url_regex)

        # We need to add a / to the beginning of the regex to prevent
        # Spack from picking up similarly named packages like:
        #   https://cran.r-project.org/src/contrib/pls_2.6-0.tar.gz
        #   https://cran.r-project.org/src/contrib/enpls_5.7.tar.gz
        #   https://cran.r-project.org/src/contrib/autopls_1.3.tar.gz
        #   https://cran.r-project.org/src/contrib/matrixpls_1.0.4.tar.gz
        url_regex = "/" + url_regex

        # We need to add a $ anchor to the end of the regex to prevent
        # Spack from picking up signature files like:
        #   .asc
        #   .md5
        #   .sha256
        #   .sig
        # However, SourceForge downloads still need to end in '/download'.
        url_regex += r"(\/download)?"
        # PyPI adds #sha256=... to the end of the URL
        url_regex += "(#sha256=.*)?"
        url_regex += "$"

        regexes.append(url_regex)

    # Build a dict version -> URL from any links that match the wildcards.
    # Walk through archive_url links first.
    # Any conflicting versions will be overwritten by the list_url links.
    versions = {}
    matched = set()
    for url in sorted(links):
        url = convert_to_posix_path(url)
        if any(re.search(r, url) for r in regexes):
            try:
                ver = spack.url.parse_version(url)
                if ver in matched:
                    continue
                versions[ver] = url
                # prevent this version from getting overwritten
                if reference_package is not None:
                    if url == reference_package.url_for_version(ver):
                        matched.add(ver)
                else:
                    extrapolated_urls = [
                        spack.url.substitute_version(u, ver) for u in archive_urls
                    ]
                    if url in extrapolated_urls:
                        matched.add(ver)
            except spack.url.UndetectableVersionError:
                continue

    for url in archive_urls:
        url = convert_to_posix_path(url)
        ver = spack.url.parse_version(url)
        if ver not in versions:
            versions[ver] = url

    return versions


def get_header(headers, header_name):
    """Looks up a dict of headers for the given header value.

    Looks up a dict of headers, [headers], for a header value given by
    [header_name].  Returns headers[header_name] if header_name is in headers.
    Otherwise, the first fuzzy match is returned, if any.

    This fuzzy matching is performed by discarding word separators and
    capitalization, so that for example, "Content-length", "content_length",
    "conTENtLength", etc., all match.  In the case of multiple fuzzy-matches,
    the returned value is the "first" such match given the underlying mapping's
    ordering, or unspecified if no such ordering is defined.

    If header_name is not in headers, and no such fuzzy match exists, then a
    KeyError is raised.
    """

    def unfuzz(header):
        return re.sub(r"[ _-]", "", header).lower()

    try:
        return headers[header_name]
    except KeyError:
        unfuzzed_header_name = unfuzz(header_name)
        for header, value in headers.items():
            if unfuzz(header) == unfuzzed_header_name:
                return value
        raise


class FetchError(spack.error.SpackError):
    """Superclass for fetch-related errors."""


class SpackWebError(spack.error.SpackError):
    """Superclass for Spack web spidering errors."""


class NoNetworkConnectionError(SpackWebError):
    """Raised when an operation can't get an internet connection."""

    def __init__(self, message, url):
        super(NoNetworkConnectionError, self).__init__(
            "No network connection: " + str(message), "URL was: " + str(url)
        )
        self.url = url
