# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
import http.client
import io
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import warnings
from http import HTTPStatus
from typing import Callable, List, NamedTuple, Optional

import spack.llnl.util.filesystem as fs

from ..error import FetchError
from .executable import which_string
from .web import SPACK_USER_AGENT, base_curl_fetch_args, check_curl_code, urlopen


class RequestInfo(NamedTuple):
    """Information about a GET request."""

    url: str
    effective_url: str
    headers: http.client.HTTPMessage


class DownloadInfo(NamedTuple):
    """Information about a download."""

    request: RequestInfo
    path: str


def create_download_info(
    *,
    url: str,
    effective_url: str = "",
    headers: Optional[http.client.HTTPMessage] = None,
    path: str = "",
) -> DownloadInfo:
    """Create a DownloadInfo object from a RequestInfo object."""
    request = RequestInfo(
        url=url, effective_url=effective_url, headers=headers or http.client.HTTPMessage()
    )
    return DownloadInfo(request=request, path=path)


class UrlStreamReader:
    """Context manager that reads from an URL stream."""

    def __init__(self, *, url: str, timeout: int):
        self.url = url
        self.timeout = timeout

    def __enter__(self) -> "UrlStreamReader":
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read(self, size: int) -> bytes:
        """Reads and returns a chunk of the response body."""
        raise NotImplementedError

    def request_info(self) -> RequestInfo:
        """Returns information about the current request."""
        raise NotImplementedError


class UrllibStreamReader(UrlStreamReader):
    """Streams a file from a URL using urllib."""

    def __enter__(self) -> UrlStreamReader:
        request = urllib.request.Request(self.url, headers={"User-Agent": SPACK_USER_AGENT})
        self._response = urlopen(request, timeout=self.timeout)
        return self

    def read(self, size: int) -> bytes:
        chunk = self._response.read(size)
        return chunk

    def request_info(self) -> RequestInfo:
        effective_url = self.url
        if isinstance(self._response, http.client.HTTPResponse):
            effective_url = self._response.geturl()
        return RequestInfo(
            url=self.url, effective_url=effective_url, headers=self._response.headers
        )


class CurlStreamReader(UrlStreamReader):
    """Streams a file from a URL using curl."""

    _curl_exe: Optional[str] = None

    def __init__(self, *, url: str, timeout: int, config_args: Optional[List[str]] = None):
        super().__init__(url=url, timeout=timeout)
        self._config_args: List[str] = config_args or []
        if CurlStreamReader._curl_exe is None:
            CurlStreamReader._curl_exe = which_string("curl", required=True)
        self._curl = CurlStreamReader._curl_exe

    def __enter__(self) -> UrlStreamReader:
        curl_args = (
            base_curl_fetch_args(
                self.url, self.timeout, status_bar=False, user_agent=SPACK_USER_AGENT
            )
            + self._config_args
        )
        curl_cmd = [self._curl] + curl_args
        self._curl_process = subprocess.Popen(
            curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        self._scheme = urllib.parse.urlparse(self.url).scheme
        assert self._curl_process.stdout is not None, "curl process stderr is None"
        self._stream = io.BufferedReader(self._curl_process.stdout)  # type: ignore[type-var]

        # curl echoes intermediate redirect responses, so we might get multiple headers
        headers = []
        while True:
            header, finished = self._get_next_header()
            headers.append(header)
            if finished:
                break

        if not headers:
            raise FetchError(f"Failed to fetch {self.url}: no headers returned")

        self._headers = headers
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._curl_process.wait()
        check_curl_code(self._curl_process.returncode)

    def read(self, size: int) -> bytes:
        return self._stream.read(size)  # type: ignore

    def request_info(self) -> RequestInfo:
        effective_url = self.url
        for h in reversed(self._headers):
            if "location" in h:
                effective_url = h["location"]
                break
        return RequestInfo(url=self.url, effective_url=effective_url, headers=self._headers[-1])

    @staticmethod
    def cookie_args(cookie) -> List[str]:
        """Returns the arguments to pass to curl to use a cookie.

        This can be used as a helper function to generate the arguments for the constructor.
        """
        return ["-j", "-b", cookie]

    def _get_next_header(self):
        """Returns the next header from the stream."""

        if self._scheme not in ("http", "https"):
            return http.client.HTTPMessage(), True

        finished = True
        status_line = self._stream.readline().decode("iso-8859-1")
        if not status_line.startswith("HTTP/"):
            raise FetchError(f"Failed to fetch {self.url}: unexpected status line: {status_line}")
        try:
            status = int(status_line.split()[1])
        except ValueError:
            raise FetchError(
                f"Failed to fetch {self.url}: cannot parse HTTP status code from {status_line}"
            )

        if 400 <= status < 600:
            raise FetchError(
                f"Failed to fetch {self.url}: {status} {HTTPStatus(int(status)).phrase}"
            )

        header = http.client.parse_headers(self._stream)
        if self._stream.peek(len(b"HTTP/")).startswith(b"HTTP/"):
            finished = False

        return header, finished


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
    method: DownloadMethod, *, extra_ars: Optional[List[str]] = None
) -> DownloadOptions:
    """Create a DownloadOptions object from a method and extra arguments."""
    return DownloadOptions(method=method, extra_args=extra_ars or [])


def download_file(
    url: str,
    *,
    destination: str,
    timeout: int = 0,
    chunk_size: int = 65536,
    options: DownloadOptions = create_download_options(DownloadMethod.URLLIB),
) -> DownloadInfo:
    """Downloads a file from the specified URL and saves it to the given path.

    Args:
        url: the URL from which the file should be downloaded.
        destination: the local file path where the downloaded file will be saved.
        timeout: timeout in seconds for the download.
        chunk_size: size of chunks to read and write during the download.
        options: options for the download of the file, including the method.
            The default is to use urllib.

    Returns:
        An object containing details about the downloaded file,
        including the original URL, effective URL after redirects, saved path,
        and response headers.
    """
    url_reader: UrlStreamReader
    if options.method == DownloadMethod.URLLIB:
        url_reader = UrllibStreamReader(url=url, timeout=timeout)
    elif options.method == DownloadMethod.CURL:
        url_reader = CurlStreamReader(url=url, timeout=timeout, config_args=options.extra_args)

    partial_file = destination + ".part"
    with url_reader as s, open(partial_file, "wb") as f:
        request_info = s.request_info()
        progress = FetchProgress.from_headers(request_info.headers, enabled=sys.stdout.isatty())
        while True:
            chunk = s.read(size=chunk_size)
            if not chunk:
                break
            f.write(chunk)
            progress.advance(len(chunk))
        progress.print(final=True)

    fs.rename(partial_file, destination)
    return DownloadInfo(request=request_info, path=destination)


def _check_headers(download_info: DownloadInfo) -> None:
    # Check if we somehow got an HTML file rather than the archive we
    # asked for.  We only look at the last content type, to handle
    # redirects properly.
    request = download_info.request
    content_types = request.headers.get("Content-Type")
    if content_types and "text/html" in content_types[-1]:
        msg = (
            f"The contents of {download_info.path or 'the archive'} fetched from "
            f"{request.url} looks like HTML. This can indicate a broken URL, "
            f"or an internet gateway issue."
        )
        if request.effective_url != request.url:
            msg += f" The URL redirected to {request.effective_url}."
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
