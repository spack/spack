import json
import re
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import llnl.util.tty as tty

import spack.config as config
import spack.error
import spack.spec
import spack.stage
import spack.util.gpg
import spack.util.url as url_util
import spack.util.web as web_util


class ExistsInBuildcache(NamedTuple):
    signed: bool
    signed_url: str
    unsigned: bool
    unsigned_url: str
    tarball: bool
    tarball_url: str


class URLBuildcacheEntry:
    """A class for managing URL-style buildcache entries

    This class manages access to a versioned buildcache entry by providing
    a means to download both the metadata (spec file) and compressed archive.
    It also provides methods for accessing the paths/urls associcated with
    buildcache entries.

    Starting with buildcache layout version 3, it is not possible to know
    the full path to a compressed archive without either building it locally,
    or else fetching and reading the metadata first.  This class provides api
    for fetching the metadata, as well as fetching the archive, and it enforces
    the need to fetch the metadata first.

    To help with downloading, this class manages two spack.spec.Stage objects
    internally, which must be destroyed when finished.  Specifically, if you
    call any of the following methods on an instance, you must eventually also
    call destroy():

        exists()
        fetch_metadata()
        fetch_archive()

    An instance of this class must be initialized, which can be accomplished
    in one of two ways: from a concrete spec and a mirror url, or else from a
    full url to an existing spec in a mirror (either signed or unsigned). The
    two methods to do this are:

        initialize_from_spec_and_mirror()
        initialize_from_spec_url()

    """

    SPEC_URL_REGEX = re.compile(r"(.+)/v([\d]+)/specs/.+")
    LAYOUT_VERSION = 3

    @classmethod
    def get_layout_version(cls):
        return cls.LAYOUT_VERSION

    def __init__(self):
        """Lazily initialize the object"""
        super().__init__()

        self.has_signed: bool = False
        self.has_unsigned: bool = False
        self.has_tarball: bool = False
        self.spec_stage: Optional[spack.stage.Stage] = None
        self.local_specfile_path = ""
        self.archive_stage: Optional[spack.stage.Stage] = None
        self.local_archive_path: str = ""
        self.signature_required: bool = False
        self.verified: bool = False
        self.mirror_url: str = ""
        self.remote_spec_url = ""
        self.remote_spec_url_signed = ""
        self.remote_spec_url_unsigned = ""
        self.remote_archive_url: str = ""
        self.remote_archive_checksum_algorithm: str = ""
        self.remote_archive_checksum_hash: str = ""
        self.spec_dict: Dict[Any, Any] = {}

        self._checked_signed = False
        self._checked_unsigned = False
        self._checked_tarball = False

    def initialize_from_spec_and_mirror(self, spec: spack.spec.Spec, mirror_url: str):
        if not spec.concrete:
            raise BuildcacheEntryError("Concrete spec required for URLBuildcacheEntry")

        self.mirror_url = mirror_url
        self.remote_spec_url_signed = self.compute_remote_spec_url(spec, mirror_url, signed=True)
        self.remote_spec_url_unsigned = self.compute_remote_spec_url(
            spec, mirror_url, signed=False
        )

    def initialize_from_spec_url(self, spec_url: str):
        """Initialized the buildcache entry from a url to a spec metadata file.  If the
        metadata url is not for a v3 spec, or otherwise does match the expected format
        or does not exist, an exception is raised."""
        rematch = URLBuildcacheEntry.SPEC_URL_REGEX.search(spec_url)

        if not rematch:
            raise BuildcacheEntryError(f"Provided url does not match expected format: {spec_url}")

        remote_layout_version = int(rematch.group(2))
        if not remote_layout_version == 3:
            raise BuildcacheEntryError(f"{spec_url} is not a v3 spec")

        self.mirror_url = rematch.group(1)

        if not web_util.url_exists(spec_url):
            raise BuildcacheEntryError(f"No spec could be found at the given url: {spec_url}")

        self.remote_spec_url = spec_url

        if self.remote_spec_url.endswith(".sig"):
            self.has_signed = True
            self.has_unsigned = False
            self.remote_spec_url_signed = spec_url
            self.remote_spec_url_unsigned = spec_url[:-4]
        else:
            self.has_signed = False
            self.has_unsigned = True
            self.remote_spec_url_unsigned = spec_url
            self.remote_spec_url_signed = f"{spec_url}.sig"

    def get_base_url(self, spec_url: str) -> str:
        rematch = URLBuildcacheEntry.SPEC_URL_REGEX.search(spec_url)
        if not rematch:
            raise BuildcacheEntryError(f"Unable to parse spec url: {spec_url}")
        return rematch.group(1)

    def compute_remote_archive_url(self, mirror_url: str, algorithm: str, checksum: str) -> str:
        rel_tarball_components = self.get_relative_tarball_components(algorithm, checksum)
        return url_util.join(mirror_url, *rel_tarball_components)

    def compute_remote_spec_url(
        self, spec: spack.spec.Spec, mirror_url: str, signed: bool = True
    ) -> str:
        url_prefix = url_util.join(mirror_url, *self.get_relative_spec_components(spec, ".spec"))
        ext = ".json.sig" if signed else ".json"
        return f"{url_prefix}{ext}"

    def _check_metadata_exists(self):
        if not self._checked_signed:
            if web_util.url_exists(self.remote_spec_url_signed):
                self.remote_spec_url = self.remote_spec_url_signed
                self.has_signed = True
            self._checked_signed = True

        if not self.has_signed and not self._checked_unsigned:
            if web_util.url_exists(self.remote_spec_url_unsigned):
                if not self.has_signed:
                    self.remote_spec_url = self.remote_spec_url_unsigned
                self.has_unsigned = True
            self._checked_unsigned = True

    def _check_archive_exists(self):
        if not self._checked_tarball:
            self.has_tarball = web_util.url_exists(self.remote_archive_url)
            self._checked_tarball = True

    def exists(self) -> ExistsInBuildcache:
        try:
            self.fetch_metadata()
            self._check_archive_exists()
        except BuildcacheEntryError as e:
            tty.debug(f"Exception checking buildcache entry existence: {e}")

        return ExistsInBuildcache(
            self.has_signed,
            self.remote_spec_url_signed,
            self.has_unsigned,
            self.remote_spec_url_unsigned,
            self.has_tarball,
            self.remote_archive_url,
        )

    def fetch_metadata(self) -> dict:
        """Retrieve metadata for the spec, yields the validated spec+ dict"""
        if self.spec_dict:
            # Only fetch the metadata once
            return self.spec_dict

        self._check_metadata_exists()

        if not self.remote_spec_url:
            raise BuildcacheEntryError(
                f"Mirror {self.mirror_url} has neither {self.remote_spec_url_signed} "
                f"nor {self.remote_spec_url_unsigned}"
            )

        self.spec_stage = spack.stage.Stage(self.remote_spec_url)

        # Fetch the spec file, or else cleanup and exit early
        try:
            self.spec_stage.create()
            self.spec_stage.fetch()
        except spack.error.FetchError as e:
            self.destroy()
            raise BuildcacheEntryError("Unable to fetch metadata") from e

        self.local_specfile_path = self.spec_stage.save_filename

        # Check spec file for validity and read it, or else cleanup and exit early
        try:
            self.spec_dict, _ = get_valid_spec_file(
                self.local_specfile_path, self.get_layout_version()
            )
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        # Retrieve the alg and hash from the spec dict, use them to build the path to
        # the tarball.
        bchecksum = self.spec_dict["binary_cache_checksum"]
        self.remote_archive_checksum_algorithm = bchecksum["hash_algorithm"]
        self.remote_archive_checksum_hash = bchecksum["hash"]
        self.remote_archive_url = self.compute_remote_archive_url(
            self.mirror_url,
            self.remote_archive_checksum_algorithm,
            self.remote_archive_checksum_hash,
        )

        return self.spec_dict

    def fetch_archive(self, allow_unsigned: bool = False):
        """Retrieve the archive file and return the local archive file path"""
        if not self.spec_dict:
            raise BuildcacheEntryError(
                "Cannot fetch archive without first fetching valid metadata"
            )

        if not allow_unsigned:
            if not self.has_signed:
                raise BuildcacheEntryError(
                    "Buildcache entry created with allow_unsigned=False, but no signed "
                    "spec file exists on mirror"
                )
            self.verified = try_verify(self.get_local_spec_path())
            if not self.verified:
                raise NoVerifyException(
                    f"Signature on {self.remote_spec_url} could not be verified"
                )

        self.archive_stage = spack.stage.Stage(self.remote_archive_url)

        # Fetch the archive file, or else cleanup and exit early
        try:
            self.archive_stage.create()
            self.archive_stage.fetch()
        except spack.error.FetchError as e:
            self.destroy()
            raise BuildcacheEntryError("Unable to fetch archive") from e

        self.local_archive_path = self.archive_stage.save_filename

        return self.local_archive_path

    def get_relative_spec_components(self, spec: spack.spec.Spec, ext: str) -> List[str]:
        spec_formatted = spec.format_path("{name}-{version}-{hash}")
        return [f"v{self.get_layout_version()}", "specs", f"{spec_formatted}{ext}"]

    def get_relative_tarball_components(self, algorithm: str, checksum: str) -> List[str]:
        return ["blobs", algorithm, checksum[:2], checksum]

    def get_relative_keys_components(self) -> List[str]:
        return [f"v{self.get_layout_version()}", "keys", "_pgp"]

    def get_relative_specs_components(self) -> List[str]:
        return [f"v{self.get_layout_version()}", "specs"]

    def get_relative_blobs_components(self) -> List[str]:
        return ["blobs"]

    def get_remote_spec_url(self):
        return self.remote_spec_url

    def get_remote_archive_url(self):
        return self.remote_archive_url

    def get_local_spec_path(self):
        return self.local_specfile_path

    def get_local_archive_path(self):
        return self.local_archive_path

    def get_signature_required(self):
        return self.signature_required

    def get_archive_checksum_algorithm(self):
        return self.remote_archive_checksum_algorithm

    def get_archive_checksum_hash(self):
        return self.remote_archive_checksum_hash

    def destroy(self):
        if self.spec_stage:
            self.spec_stage.destroy()
            self.spec_stage = None
        if self.archive_stage:
            self.archive_stage.destroy()
            self.archive_stage = None

    def is_verified(self):
        return self.verified

    def get_spec_dict(self) -> Dict:
        return self.spec_dict


def create_url_buildcache_entry(layout_version: int) -> URLBuildcacheEntry:
    if layout_version == 3:
        return URLBuildcacheEntry()
    else:
        raise UnknownBuildcacheLayoutError(
            f"Buildcache layout version {layout_version} is unknown"
        )


def get_valid_spec_file(path: str, max_supported_layout: int) -> Tuple[Dict, int]:
    """Read and validate a spec file, returning the spec dict with its layout version, or raising
    InvalidMetadataFile if invalid."""
    try:
        with open(path, "rb") as f:
            binary_content = f.read()
    except OSError:
        raise InvalidMetadataFile(f"No such file: {path}")

    # In the future we may support transparently decompressing compressed spec files.
    if binary_content[:2] == b"\x1f\x8b":
        raise InvalidMetadataFile("Compressed spec files are not supported")

    try:
        as_string = binary_content.decode("utf-8")
        if path.endswith(".json.sig"):
            spec_dict = spack.spec.Spec.extract_json_from_clearsig(as_string)
        else:
            spec_dict = json.loads(as_string)
    except Exception as e:
        raise InvalidMetadataFile(f"Could not parse {path} due to: {e}") from e

    # Ensure this version is not too new.
    try:
        layout_version = int(spec_dict.get("buildcache_layout_version", 0))
    except ValueError as e:
        raise InvalidMetadataFile("Could not parse layout version") from e

    if layout_version > max_supported_layout:
        raise InvalidMetadataFile(
            f"Layout version {layout_version} is too new for this version of Spack"
        )

    return spec_dict, layout_version


def try_verify(specfile_path):
    """Utility function to attempt to verify a local file.  Assumes the
    file is a clearsigned signature file.

    Args:
        specfile_path (str): Path to file to be verified.

    Returns:
        ``True`` if the signature could be verified, ``False`` otherwise.
    """
    suppress = config.get("config:suppress_gpg_warnings", False)

    try:
        spack.util.gpg.verify(specfile_path, suppress_warnings=suppress)
    except Exception:
        return False

    return True


class MirrorURLAndVersion:
    url: str
    version: int

    def __init__(self, url: str, version: int):
        self.url = url
        self.version = version

    def __str__(self):
        return f"{self.url}__v{self.version}"

    def __eq__(self, other):
        if isinstance(other, MirrorURLAndVersion):
            return self.url == other.url and self.version == other.version
        return False

    def __hash__(self):
        return hash((self.url, self.version))

    @classmethod
    def from_string(cls, s: str):
        parts = s.split("__v")
        return cls(parts[0], int(parts[1]))


class MirrorForSpec:
    url_and_version: MirrorURLAndVersion
    spec: spack.spec.Spec

    def __init__(self, url_and_version: MirrorURLAndVersion, spec: spack.spec.Spec):
        self.url_and_version = url_and_version
        self.spec = spec


class InvalidMetadataFile(spack.error.SpackError):
    pass


class BuildcacheEntryError(spack.error.SpackError):
    """Raised for problems finding or accessing binary cache entry on mirror"""

    pass


class NoVerifyException(BuildcacheEntryError):
    """
    Raised if file fails signature verification.
    """

    pass


class UnknownBuildcacheLayoutError(BuildcacheEntryError):
    """Raised when unrecognized buildcache layout version is encountered"""

    pass
