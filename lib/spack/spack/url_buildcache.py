# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import datetime
import gzip
import json
import os
import re
import shutil
import tempfile
from typing import Any, Dict, List, NamedTuple, Optional, Tuple

import jsonschema

import llnl.util.tty as tty

import spack.config as config
import spack.error
import spack.hash_types as ht
import spack.spec
import spack.stage
import spack.util.crypto
import spack.util.gpg
import spack.util.url as url_util
import spack.util.web as web_util
from spack.schema.url_buildcache_manifest import schema as buildcache_manifest_schema


class ExistsInBuildcache(NamedTuple):
    signed: bool
    signed_url: str
    unsigned: bool
    unsigned_url: str
    tarball: bool
    tarball_url: str


class BlobRecord:
    def __init__(
        self,
        content_length: int,
        content_type: str,
        compression_alg: str,
        checksum_alg: str,
        checksum: str,
    ) -> None:
        self.content_length = content_length
        self.content_type = content_type
        self.compression_alg = compression_alg
        self.checksum_alg = checksum_alg
        self.checksum = checksum

    @classmethod
    def from_json(cls, json_object):
        return BlobRecord(
            json_object["content-length"],
            json_object["content-type"],
            json_object["compression"],
            json_object["checksum-algorithm"],
            json_object["checksum"],
        )

    def to_json(self):
        return {
            "content-length": self.content_length,
            "content-type": self.content_type,
            "compression": self.compression_alg,
            "checksum-algorithm": self.checksum_alg,
            "checksum": self.checksum,
        }


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
    def get_layout_version(cls) -> int:
        return cls.LAYOUT_VERSION

    def __init__(self, push_url_base: str, spec: Optional[spack.spec.Spec] = None):
        """Lazily initialize the object"""
        super().__init__()

        self.mirror_url: str = push_url_base
        self.spec = spec

        self.has_manifest: bool = False
        self.has_metadata: bool = False
        self.has_tarball: bool = False
        self.spec_stage: Optional[spack.stage.Stage] = None
        self.local_specfile_path = ""
        self.archive_stage: Optional[spack.stage.Stage] = None
        self.local_archive_path: str = ""
        self.verified: bool = False

        self.remote_manifest_url = ""
        self.remote_spec_url = ""
        self.remote_archive_url: str = ""
        self.remote_archive_checksum_algorithm: str = ""
        self.remote_archive_checksum_hash: str = ""
        self.spec_dict: Dict[Any, Any] = {}

        self.data: List[BlobRecord] = []

        self._checked_exists = False

        if self.spec:
            self.read_manifest(self.get_manifest_url(self.spec, self.mirror_url))

    def get_base_url(self, spec_url: str) -> str:
        rematch = URLBuildcacheEntry.SPEC_URL_REGEX.search(spec_url)
        if not rematch:
            raise BuildcacheEntryError(f"Unable to parse spec url: {spec_url}")
        return rematch.group(1)

    def compute_remote_archive_url(self, mirror_url: str) -> str:
        rel_tarball_components = self.get_relative_tarball_components()
        return url_util.join(mirror_url, *rel_tarball_components)

    @classmethod
    def compute_remote_spec_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        # TODO: This will always be the same, signed or unsiged "blah.manifest.json"
        return url_util.join(mirror_url, *cls.get_relative_spec_components(spec, ".spec.json.sig"))

    def _check_metadata_exists(self):
        if self.remote_spec_url:
            self.has_metadata = web_util.url_exists(self.remote_spec_url)

    def _check_archive_exists(self):
        if self.remote_archive_url:
            self.has_tarball = web_util.url_exists(self.remote_archive_url)

    @classmethod
    def get_manifest_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        return url_util.join(mirror_url, *cls.get_relative_spec_components(spec, ".manifest.json"))

    def _maybe_verify_and_extract(self, manifest_contents: str, verify: bool = False) -> dict:
        magic_string = "-----BEGIN PGP SIGNED MESSAGE-----"
        if manifest_contents.startswith(magic_string):
            if verify:
                # write to file
                # try to verify and raise if we fail
                tmpdir = tempfile.mkdtemp()
                try:
                    manifest_path = os.path.join(tmpdir, "manifest.json.sig")
                    with open(manifest_path, "wb", encoding="utf-8") as fd:
                        fd.write(manifest_contents)
                    if not try_verify(manifest_path):
                        raise NoVerifyException(
                            f"Signature on {self.remote_spec_url} could not be verified"
                        )
                finally:
                    shutil.rmtree(tmpdir)

            return spack.spec.Spec.extract_json_from_clearsig(manifest_contents)

        return json.loads(manifest_contents)

    def read_manifest(self, manifest_url: Optional[str] = None, verify_signature: bool = False) -> None:
        """Read and process the the buildcache entry manifest.

        If no manifest url is provided, build the url from the internal spec and
        base push url."""
        if not manifest_url:
            if not self.spec or not self.mirror_url:
                raise BuildcacheEntryError(
                    "Either manifest url or spec and mirror are required to read manifest"
                )
            manifest_url = self.get_manifest_url(self.spec, self.mirror_url)

        self.remote_manifest_url = manifest_url
        manifest_contents = ""

        try:
            _, _, manifest_file = web_util.read_from_url(manifest_url)
            manifest_contents = codecs.getreader("utf-8")(manifest_file).read()
        except (web_util.SpackWebError, OSError) as e:
            tty.error(f"Error reading specfile: {manifest_url}: {e}")

        if not manifest_contents:
            raise BuildcacheEntryError("Unable to read manifest or manifest empty")

        manifest_contents = self._maybe_verify_and_extract(manifest_contents, verify=verify_signature)

        jsonschema.validate(manifest_contents, buildcache_manifest_schema)

        if manifest_contents["version"] != 3:
            raise BuildcacheEntryError("Layout version mismatch in fetched manifest")

        self.data = []

        # Load the list of blob records, and find the ones associated with the spec and archive
        for obj in manifest_contents["data"]:
            record = BlobRecord.from_json(obj)
            self.data.append(record)
            blob_url = url_util.join(
                self.mirror_url,
                *self.get_relative_blobs_components(),
                record.checksum_alg,
                record.checksum[:2],
                record.checksum,
            )
            if record.content_type.startswith("spec"):
                self.remote_spec_url = blob_url
            elif record.content_type.startswith("tarball"):
                self.remote_archive_url = blob_url

        self.has_manifest = True
        self._checked_exists = False

    def exists(self) -> bool:
        if not self._checked_exists:
            try:
                self.read_manifest()
            except BuildcacheEntryError:
                return False

            self._check_metadata_exists()
            self._check_archive_exists()
            self._checked_exists = True

        return self.has_metadata and self.has_tarball

    def fetch_metadata(self) -> dict:
        """Retrieve metadata for the spec, yields the validated spec+ dict"""
        if self.spec_dict:
            # Only fetch the metadata once
            return self.spec_dict

        # Reading the manifest will either successfully compute the remote
        # spec url, or else raise
        self.read_manifest()

        self.spec_stage = spack.stage.Stage(self.remote_spec_url)

        # Fetch the spec file, or else cleanup and exit early
        try:
            self.spec_stage.create()
            self.spec_stage.fetch()
        except spack.error.FetchError as e:
            self.destroy()
            raise BuildcacheEntryError("Unable to fetch metadata") from e

        # Uncompress fetched data here, so local specfile path is useful?

        self.local_specfile_path = self.spec_stage.save_filename

        # Check spec file for validity and read it, or else cleanup and exit early
        try:
            spec_dict, _ = get_valid_spec_file(self.local_specfile_path, self.get_layout_version())
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        try:
            self.spec = spack.spec.Spec.from_dict(spec_dict["spec"])
        except Exception as err:
            raise BuildcacheEntryError("Fetched spec dict does not contain valid spec") from err

        self._set_spec_dict(spec_dict)

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

    @classmethod
    def get_relative_spec_components(cls, spec: spack.spec.Spec, ext: str) -> List[str]:
        spec_formatted = spec.format_path("{name}-{version}-{hash}")
        return [f"v{cls.get_layout_version()}", "specs", f"{spec_formatted}{ext}"]

    def get_relative_tarball_components(self) -> List[str]:
        return [
            "blobs",
            self.remote_archive_checksum_algorithm,
            self.remote_archive_checksum_hash[:2],
            self.remote_archive_checksum_hash,
        ]

    @classmethod
    def get_relative_keys_components(cls) -> List[str]:
        return [f"v{cls.get_layout_version()}", "keys", "_pgp"]

    @classmethod
    def get_relative_specs_components(cls) -> List[str]:
        return [f"v{cls.get_layout_version()}", "specs"]

    @classmethod
    def get_relative_blobs_components(cls) -> List[str]:
        return ["blobs"]

    def get_remote_spec_url(self):
        return self.remote_spec_url

    def get_remote_archive_url(self):
        return self.remote_archive_url

    def get_local_spec_path(self):
        return self.local_specfile_path

    def get_local_archive_path(self):
        return self.local_archive_path

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

    def push(
        self,
        spec: spack.spec.Spec,
        tarball_path: str,
        checksum_algorithm: str,
        tarball_checksum: str,
        tmpdir: str,
        signing_key: Optional[str],
    ) -> None:
        spec_dict = spec.to_dict(hash=ht.dag_hash)
        layout_version = self.get_layout_version()
        spec_dict["buildcache_layout_version"] = layout_version
        spec_dict["binary_cache_checksum"] = {
            "hash_algorithm": checksum_algorithm,
            "hash": tarball_checksum,
        }
        tarball_content_length = os.stat(tarball_path).st_size
        compression = "gzip"
        spec_dict["archive_size"] = tarball_content_length
        spec_dict["archive_timestamp"] = datetime.datetime.now().astimezone().isoformat()
        spec_dict["archive_compression"] = compression

        if self.has_tarball:
            web_util.remove_url(self.remote_archive_url)
        if self.has_metadata:
            web_util.remove_url(self.remote_spec_url)
        if self.has_manifest:
            web_util.remove_url(self.remote_manifest_url)

        self.remote_archive_url = url_util.join(
            self.mirror_url,
            *self.get_relative_blobs_components(),
            checksum_algorithm,
            tarball_checksum[:2],
            tarball_checksum,
        )

        # push the archive/tarball blob to the remote
        web_util.push_to_url(tarball_path, self.remote_archive_url, keep_original=False)

        self.data = []
        self.data.append(
            BlobRecord(
                tarball_content_length,
                "tarball-v1",
                compression,
                checksum_algorithm,
                tarball_checksum,
            )
        )

        # compress the spec dict and compute its checksum
        metadata_checksum = ""
        specfile = os.path.join(tmpdir, f"{spec.dag_hash()}.spec.json")
        with open(specfile, "wb", encoding="utf-8") as f:
            compressed_bytes = gzip.compress(json.dumps(spec_dict).encode("utf-8"), compresslevel=6, mtime=0)
            f.write(compressed_bytes)
            hasher = spack.util.crypto.hash_fun_for_algo(checksum_algorithm)()
            hasher.update(compressed_bytes)
            metadata_checksum = hasher.hexdigest()

        metadata_size = os.stat(specfile).st_size

        self.remote_spec_url = url_util.join(
            self.mirror_url,
            *self.get_relative_blobs_components(),
            checksum_algorithm,
            metadata_checksum[:2],
            metadata_checksum,
        )

        # push the metadata/spec blob to the remote
        web_util.push_to_url(specfile, self.remote_spec_url, keep_original=False)

        self.data.append(
            BlobRecord(
                metadata_size,
                "spec-v6",
                compression,
                checksum_algorithm,
                metadata_checksum,
            )
        )

        # generate the manifest
        manifest = {
            "version": self.get_layout_version(),
            "data": [record.to_json() for record in self.data],
        }

        # write the manifest to a temporary location
        manifest_path = os.path.join(tmpdir, f"{spec.dag_hash()}.manifest.json")
        with open(manifest_path, "wb", encoding="utf-8") as f:
            json.dump(manifest, f)

        # possibly sign the manifest
        if signing_key:
            manifest_path = sign_specfile(signing_key, manifest_path)

        self.remote_manifest_url = url_util.join(
            self.mirror_url,
            *self.get_relative_spec_components(spec, ".manifest.json"),
        )

        # push the manifest file to the remote
        web_util.push_to_url(manifest_path, self.remote_manifest_url, keep_original=False)


class URLBuildcacheEntryV2(URLBuildcacheEntry):
    SPEC_URL_REGEX = re.compile(r"(.+)/build_cache/.+")
    LAYOUT_VERSION = 2

    @classmethod
    def get_layout_version(cls) -> int:
        return cls.LAYOUT_VERSION

    @classmethod
    def compute_remote_spec_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        return url_util.join(mirror_url, *cls.get_relative_spec_components(spec, ".spec.json.sig"))

    def initialize_from_spec_url(self, spec_url: str):
        try:
            return super().initialize_from_spec_url(spec_url)
        except BuildcacheEntryError:
            if spec_url.endswith(".sig"):
                return super().initialize_from_spec_url(spec_url[:-4])

    def read_manifest(self, manifest_url: Optional[str] = None) -> None:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

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
            spec_dict, _ = get_valid_spec_file(self.local_specfile_path, self.get_layout_version())
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        try:
            self.spec = spack.spec.Spec.from_dict(spec_dict["spec"])
        except Exception as err:
            raise BuildcacheEntryError("Fetched spec dict does not contain valid spec") from err

        self._set_spec_dict(spec_dict)

        return self.spec_dict

    def push(
        self,
        spec: spack.spec.Spec,
        tarball_path: str,
        tarball_checksum_algo: str,
        tarball_checksum: str,
        tmpdir: str,
        push_url_base: str,
        signing_key: Optional[str],
    ) -> None:
        raise BuildcacheEntryError("Spack can no longer push v2 buildcache entries")


def get_url_buildcache_class(layout_version: int) -> type:
    if layout_version == 2:
        return URLBuildcacheEntryV2
    elif layout_version == 3:
        return URLBuildcacheEntry
    else:
        raise UnknownBuildcacheLayoutError(
            f"Cannot create buildcache class for unknown layout version {layout_version}"
        )


def create_url_buildcache_entry(layout_version: int) -> URLBuildcacheEntry:
    if layout_version == 3:
        return URLBuildcacheEntry()
    elif layout_version == 2:
        return URLBuildcacheEntryV2()
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


def sign_specfile(key: str, specfile_path: str) -> str:
    """sign and return the path to the signed specfile"""
    signed_specfile_path = f"{specfile_path}.sig"
    spack.util.gpg.sign(key, specfile_path, signed_specfile_path, clearsign=True)
    return signed_specfile_path


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
