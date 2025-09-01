# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import abc
import contextlib
import enum
import http.client
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import warnings
from http import HTTPStatus
from http.client import HTTPMessage
from typing import Any, Callable, Generator, List, NamedTuple, Optional, Tuple

from spack.vendor.typing_extensions import Protocol

import spack.llnl.util.filesystem as fs
from spack.llnl.util import tty

from ..error import FetchError
from .executable import which_string
from .web import (
    SPACK_USER_AGENT,
    DetailedHTTPError,
    base_curl_fetch_args,
    check_curl_code,
    urlopen,
)


class UrlStream(Protocol):
    """A stream of bytes from a URL."""

    #: URL of the initial request.
    url: str

    #: Header of the final response.
    headers: HTTPMessage

    @abc.abstractmethod
    def read(self, size: int) -> bytes:
        """Reads and returns a chunk of the final response body."""
        raise NotImplementedError

    @abc.abstractmethod
    def geturl(self) -> str:
        """Returns the effective URL of the request"""
        raise NotImplementedError


class UrllibStream(UrlStream):
    def __init__(self, *, url: str, response):
        # We cannot return a raw response because we need the original url in some place
        # and HTTPResponse.url is the same as geturl()
        self.url = url
        self.headers = response.headers
        self._response = response

    def read(self, size: int) -> bytes:
        return self._response.read(size)

    def geturl(self) -> str:
        return self._response.geturl()


@contextlib.contextmanager
def urllib_stream(url: str, timeout: int) -> Generator[UrlStream, Any, None]:
    request = urllib.request.Request(url, headers={"User-Agent": SPACK_USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        yield UrllibStream(url=url, response=response)


class CurlStream(UrlStream):
    """Streams a file from a URL using curl."""

    def __init__(self, *, url: str, headers: HTTPMessage, effective_url: str, stream):
        self.url = url
        self.headers = headers
        self._effective_url = effective_url
        self._stream = stream

    def read(self, size: int) -> bytes:
        return self._stream.read(size)

    def geturl(self) -> str:
        return self._effective_url


def curl_cookie_args(cookie) -> List[str]:
    """Returns the arguments to pass to curl to use a cookie.

    This can be used as a helper function to generate the arguments for the constructor.
    """
    return ["-j", "-b", cookie]


@contextlib.contextmanager
def curl_stream(
    *, url: str, timeout: int, config_args: Optional[List[str]] = None
) -> Generator[UrlStream, Any, None]:
    config_args = config_args or []
    cmd = [which_string("curl", required=True)]
    cmd.extend(base_curl_fetch_args(url, timeout, status_bar=False, user_agent=SPACK_USER_AGENT))
    cmd.extend(config_args)
    with _start_curl_process(cmd) as curl_process:
        scheme = urllib.parse.urlparse(url).scheme
        assert curl_process.stdout is not None, "curl process stdout is None"
        stream = curl_process.stdout
        effective_url = url
        if scheme not in ("http", "https"):
            headers = HTTPMessage()
        else:
            # curl echoes intermediate redirect responses, so we might get multiple responses
            finished = False
            while not finished:
                headers, effective_url, finished = _next_http_headers(
                    url=effective_url, stream=stream
                )
        yield CurlStream(url=url, headers=headers, effective_url=effective_url, stream=stream)
    check_curl_code(curl_process.returncode)


@contextlib.contextmanager
def _start_curl_process(curl_cmd):
    with subprocess.Popen(
        curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    ) as curl_process:
        yield curl_process


def _next_http_headers(url, stream) -> Tuple[http.client.HTTPMessage, str, bool]:
    """Returns the next headers from the stream."""

    finished = True
    status_line = stream.readline().decode("iso-8859-1")
    if not status_line.startswith("HTTP/"):
        raise FetchError(f"Failed to fetch {url}: unexpected status line: {status_line}")
    try:
        status = int(status_line.split()[1])
    except ValueError:
        raise FetchError(
            f"Failed to fetch {url}: cannot parse HTTP status code from {status_line}"
        )

    headers = http.client.parse_headers(stream)
    if 400 <= status < 600:
        raise DetailedHTTPError(
            urllib.request.Request(url), status, HTTPStatus(status).phrase, headers, None
        )

    elif 300 <= status < 400:
        finished = False

    effective_url = headers.get("location", url)
    return headers, effective_url, finished


class FetchProgress:
    #: Characters to rotate in the spinner.
    spinner = ["|", "/", "-", "\\"]

    def __init__(
        self,
        total_bytes: Optional[int] = None,
        enabled: bool = True,
        get_time: Callable[[], float] = time.time,
    ) -> None:
        """Initialize a FetchProgress instance.
        Args:
            total_bytes: Total number of bytes to download, if known.
            enabled: Whether to print progress information.
            get_time: Function to get the current time."""
        #: Number of bytes downloaded so far.
        self.current_bytes = 0
        #: Delta time between progress prints
        self.delta = 0.1
        #: Whether to print progress information.
        self.enabled = enabled
        #: Function to get the current time.
        self.get_time = get_time
        #: Time of last progress print to limit output
        self.last_printed = 0.0
        #: Time of start of download
        self.start_time = get_time() if enabled else 0.0
        #: Total number of bytes to download, if known.
        self.total_bytes = total_bytes if total_bytes and total_bytes > 0 else 0
        #: Index of spinner character to print (used if total bytes is unknown)
        self.index = 0

    @classmethod
    def from_headers(
        cls,
        headers: http.client.HTTPMessage,
        enabled: bool = True,
        get_time: Callable[[], float] = time.time,
    ) -> "FetchProgress":
        """Create a FetchProgress instance from HTTP headers."""
        # headers.get is case-insensitive if it's from a HTTPResponse object.
        content_length = headers.get("Content-Length")
        try:
            total_bytes = int(content_length) if content_length else None
        except ValueError:
            total_bytes = None
        return cls(total_bytes=total_bytes, enabled=enabled, get_time=get_time)

    def advance(self, num_bytes: int, out=sys.stdout) -> None:
        if not self.enabled:
            return
        self.current_bytes += num_bytes
        self.print(out=out)

    def print(self, final: bool = False, out=sys.stdout) -> None:
        if not self.enabled:
            return
        current_time = self.get_time()
        if self.last_printed + self.delta < current_time or final:
            self.last_printed = current_time
            # print a newline if this is the final update
            maybe_newline = "\n" if final else ""
            # if we know the total bytes, show a percentage, otherwise a spinner
            if self.total_bytes > 0:
                percentage = min(100 * self.current_bytes / self.total_bytes, 100.0)
                percent_or_spinner = f"[{percentage:3.0f}%] "
            else:
                # only show the spinner if we are not at 100%
                if final:
                    percent_or_spinner = "[100%] "
                else:
                    percent_or_spinner = f"[ {self.spinner[self.index]}  ] "
                self.index = (self.index + 1) % len(self.spinner)

            print(
                f"\r    {percent_or_spinner}{_format_bytes(self.current_bytes)} "
                f"@ {_format_speed(self.current_bytes, current_time - self.start_time)}"
                f"{maybe_newline}",
                end="",
                flush=True,
                file=out,
            )


class DownloadMethod(enum.Enum):
    URLLIB = enum.auto()
    CURL = enum.auto()


class DownloadOptions(NamedTuple):
    """Options for downloading a file."""

    method: DownloadMethod = DownloadMethod.URLLIB
    extra_args: List[str] = []


def create_download_options(
    method: DownloadMethod, *, extra_args: Optional[List[str]] = None
) -> DownloadOptions:
    """Create a DownloadOptions object from a method and extra arguments."""
    return DownloadOptions(method=method, extra_args=extra_args or [])


def download_file(
    url: str,
    *,
    destination: str,
    timeout: int = 0,
    chunk_size: int = 65536,
    options: DownloadOptions = create_download_options(DownloadMethod.URLLIB),
) -> str:
    """Downloads a file from the specified URL and saves it to the given path.

    Args:
        url: the URL from which the file should be downloaded.
        destination: the local file path where the downloaded file will be saved.
        timeout: timeout in seconds for the download.
        chunk_size: size of chunks to read and write during the download.
        options: options for the download of the file, including the method.
            The default is to use urllib.

    Returns:
        The effective URL of the request.
    """
    if options.method == DownloadMethod.URLLIB:
        url_reader = urllib_stream(url=url, timeout=timeout)
    elif options.method == DownloadMethod.CURL:
        url_reader = curl_stream(url=url, timeout=timeout, config_args=options.extra_args)

    partial_file = destination + ".part"
    with url_reader as s, open(partial_file, "wb") as f:
        tty.msg(f"Fetching {url}")
        _check_headers(
            url=s.url, effective_url=s.geturl(), headers=s.headers, destination=destination
        )
        progress = FetchProgress.from_headers(s.headers, enabled=sys.stdout.isatty())
        while True:
            chunk = s.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            progress.advance(len(chunk))
        progress.print(final=True)
    fs.rename(partial_file, destination)
    return s.geturl()


def _check_headers(
    *, url: str, effective_url: str = "", headers: http.client.HTTPMessage, destination: str = ""
) -> None:
    # Check if we somehow got an HTML file rather than the archive we
    # asked for.  We only look at the last content type, to handle
    # redirects properly.
    if "text/html" in headers.get("Content-Type", ""):
        msg = (
            f"The contents of {destination or 'the archive'} fetched from {url} looks like HTML. "
            f"This can indicate a broken URL, or an internet gateway issue."
        )
        if effective_url != url:
            msg += f" The URL redirected to {effective_url}."
        warnings.warn(msg)


def _format_speed(total_bytes: int, elapsed: float) -> str:
    """Return a human-readable average download speed string."""
    elapsed = 1 if elapsed <= 0 else elapsed  # avoid divide by zero
    speed = total_bytes / elapsed
    if speed >= 1e9:
        return f"{speed / 1e9:6.1f} GB/s"
    elif speed >= 1e6:
        return f"{speed / 1e6:6.1f} MB/s"
    elif speed >= 1e3:
        return f"{speed / 1e3:6.1f} KB/s"
    return f"{speed:6.1f}  B/s"


def _format_bytes(total_bytes: int) -> str:
    """Return a human-readable total bytes string."""
    if total_bytes >= 1e9:
        return f"{total_bytes / 1e9:7.2f} GB"
    elif total_bytes >= 1e6:
        return f"{total_bytes / 1e6:7.2f} MB"
    elif total_bytes >= 1e3:
        return f"{total_bytes / 1e3:7.2f} KB"
    return f"{total_bytes:7.2f}  B"
