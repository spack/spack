# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import enum
import gzip
import json
import os
import re
import shutil
import tempfile
from typing import Any, Dict, List, Optional, Tuple

import jsonschema

import llnl.util.filesystem as fsys

import spack.config as config
import spack.error
import spack.hash_types as ht
import spack.spec
import spack.stage
import spack.util.crypto
import spack.util.gpg
import spack.util.url as url_util
import spack.util.web as web_util
from spack.database import INDEX_JSON_FILE
from spack.schema.url_buildcache_manifest import schema as buildcache_manifest_schema

INDEX_HASH_FILE = "index.json.hash"


class BuildcacheComponent(enum.Enum):
    SPECS = enum.auto()
    BLOBS = enum.auto()
    INDICES = enum.auto()
    KEYS = enum.auto()
    INDEX = enum.auto()
    INDEX_HASH = enum.auto()
    SPEC = enum.auto()
    TARBALL = enum.auto()


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


class BuildcacheManifest:
    def __init__(self, layout_version: int, data: Optional[List[BlobRecord]] = None):
        self.version: int = layout_version
        if data:
            self.data: List[BlobRecord] = [
                BlobRecord(
                    rec.content_length,
                    rec.content_type,
                    rec.compression_alg,
                    rec.checksum_alg,
                    rec.checksum,
                )
                for rec in data
            ]
        else:
            self.data = []

    def to_json(self):
        return {"version": self.version, "data": [rec.to_json() for rec in self.data]}

    @classmethod
    def from_json(cls, manifest_json: Dict[str, Any]) -> "BuildcacheManifest":
        jsonschema.validate(manifest_json, buildcache_manifest_schema)
        return BuildcacheManifest(
            layout_version=manifest_json["version"],
            data=[BlobRecord.from_json(blob_json) for blob_json in manifest_json["data"]],
        )

    def get_blob_records(self, content_type: str) -> List[BlobRecord]:
        matches: List[BlobRecord] = []

        for record in self.data:
            if record.content_type == content_type:
                # matches.append(BlobRecord.from_json(record.to_json()))
                matches.append(record)

        if matches:
            return matches

        raise NoSuchBlobException(f"Manifest has no blobs of type {content_type}")


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
    call either of the following methods on an instance, you must eventually also
    call destroy():

        fetch_metadata()
        fetch_archive()

    """

    SPEC_URL_REGEX = re.compile(r"(.+)/v([\d]+)/specs/.+")
    LAYOUT_VERSION = 3
    INDEX_VERSION = "index-v7"
    SPEC_VERSION = "spec-v6"
    TARBALL_VERSION = "tarball-v1"
    COMPONENT_PATHS = {
        BuildcacheComponent.BLOBS: ["blobs"],
        BuildcacheComponent.INDICES: [f"v{LAYOUT_VERSION}", "specs"],
        BuildcacheComponent.INDEX: [f"v{LAYOUT_VERSION}", "specs", INDEX_JSON_FILE],
        BuildcacheComponent.INDEX_HASH: [f"v{LAYOUT_VERSION}", "specs", INDEX_HASH_FILE],
        BuildcacheComponent.KEYS: [f"v{LAYOUT_VERSION}", "keys", "_pgp"],
        BuildcacheComponent.SPECS: [f"v{LAYOUT_VERSION}", "specs"],
    }

    def __init__(self, push_url_base: str, spec: Optional[spack.spec.Spec] = None):
        """Lazily initialize the object"""
        self.mirror_url: str = push_url_base
        self.spec: Optional[spack.spec.Spec] = spec
        self.manifest: Optional[BuildcacheManifest] = None
        self.remote_manifest_url: str = ""
        self.stages: Dict[BlobRecord, spack.stage.Stage] = {}

    @classmethod
    def get_layout_version(cls) -> int:
        return cls.LAYOUT_VERSION

    @classmethod
    def get_base_url(cls, spec_url: str) -> str:
        rematch = cls.SPEC_URL_REGEX.search(spec_url)
        if not rematch:
            raise BuildcacheEntryError(f"Unable to parse spec url: {spec_url}")
        return rematch.group(1)

    @classmethod
    def get_relative_path_components(cls, component: BuildcacheComponent) -> List[str]:
        return cls.COMPONENT_PATHS[component]

    @classmethod
    def get_manifest_filename(cls, spec: spack.spec.Spec) -> str:
        spec_formatted = spec.format_path("{name}-{version}-{hash}")
        return f"{spec_formatted}.manifest.json"

    @classmethod
    def get_manifest_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        path_components = cls.get_relative_path_components(BuildcacheComponent.SPECS)
        return url_util.join(mirror_url, *path_components, cls.get_manifest_filename(spec))

    @classmethod
    def content_type_to_component(cls, content_type: str) -> BuildcacheComponent:
        if content_type == cls.SPEC_VERSION:
            return BuildcacheComponent.SPEC
        elif content_type == cls.TARBALL_VERSION:
            return BuildcacheComponent.TARBALL
        elif content_type == cls.INDEX_VERSION:
            return BuildcacheComponent.INDEX

        raise BuildcacheEntryError(f"Unrecognized content type: {content_type}")

    @classmethod
    def component_to_content_type(cls, component: BuildcacheComponent) -> str:
        if component == BuildcacheComponent.SPEC:
            return cls.SPEC_VERSION
        elif component == BuildcacheComponent.TARBALL:
            return cls.TARBALL_VERSION
        elif component == BuildcacheComponent.INDEX:
            return cls.INDEX_VERSION

        raise BuildcacheEntryError(f"Not a blob component: {component}")

    def get_local_spec_path(self):
        return self.get_staged_blob_path(self.get_blob_record(BuildcacheComponent.SPEC))

    def get_local_archive_path(self):
        return self.get_staged_blob_path(self.get_blob_record(BuildcacheComponent.TARBALL))

    def get_blob_record(self, blob_type: BuildcacheComponent) -> BlobRecord:
        """Return the first blob record of the given type"""
        if not self.manifest:
            raise BuildcacheEntryError("Read manifest before accessing blob records")

        records = self.manifest.get_blob_records(self.component_to_content_type(blob_type))

        if len(records) == 0:
            raise BuildcacheEntryError(f"Manifest has no blob record of type {blob_type}")

        return records[0]

    def check_blob_exists(self, record: BlobRecord) -> bool:
        blob_url = self.get_blob_url(record)
        return web_util.url_exists(blob_url)

    @classmethod
    def get_blob_path_components(cls, record: BlobRecord) -> List[str]:
        return [
            *cls.get_relative_path_components(BuildcacheComponent.BLOBS),
            record.checksum_alg,
            record.checksum[:2],
            record.checksum,
        ]

    def get_blob_url(self, record: BlobRecord) -> str:
        return url_util.join(self.mirror_url, *self.get_blob_path_components(record))

    def fetch_blob(self, record: BlobRecord) -> str:
        """Given a blob record, find associated blob in manifest and stage it

        Returns the local path to the staged blob
        """
        if record not in self.stages:
            blob_url = self.get_blob_url(record)
            blob_stage = spack.stage.Stage(blob_url)

            # Fetch the blob, or else cleanup and exit early
            try:
                blob_stage.create()
                blob_stage.fetch()
            except spack.error.FetchError as e:
                self.destroy()
                raise BuildcacheEntryError(f"Unable to fetch blob from {blob_url}") from e

            # Raises if checksum does not match expectation
            validate_checksum(blob_stage.save_filename, record.checksum_alg, record.checksum)

            self.stages[record] = blob_stage

        return self.get_staged_blob_path(record)

    def get_staged_blob_path(self, record: BlobRecord) -> str:
        if record not in self.stages:
            raise BuildcacheEntryError(f"Blob not staged: {record}")

        return self.stages[record].save_filename

    def exists(self, components: List[BuildcacheComponent]) -> bool:
        """Check whether blobs exist for all specified components

        Returns True if there is a blob present in the mirror for every
        given component type.
        """
        try:
            self.read_manifest(verify_signature=False)
        except BuildcacheEntryError:
            return False

        if not self.manifest:
            return False

        for component in components:
            component_blobs = self.manifest.get_blob_records(
                self.component_to_content_type(component)
            )

            if len(component_blobs) == 0:
                return False

            if not self.check_blob_exists(component_blobs[0]):
                return False

        return True

    def _maybe_verify_and_extract(self, manifest_contents: str, verify: bool = False) -> dict:
        magic_string = "-----BEGIN PGP SIGNED MESSAGE-----"
        if manifest_contents.startswith(magic_string):
            if verify:
                # Rry to verify and raise if we fail
                tmpdir = tempfile.mkdtemp()
                try:
                    manifest_path = os.path.join(tmpdir, "manifest.json.sig")
                    with open(manifest_path, "w", encoding="utf-8") as fd:
                        fd.write(manifest_contents)
                    if not try_verify(manifest_path):
                        raise NoVerifyException(
                            f"Signature on {self.remote_manifest_url} could not be verified"
                        )
                finally:
                    shutil.rmtree(tmpdir)

            return spack.spec.Spec.extract_json_from_clearsig(manifest_contents)
        else:
            if verify:
                raise NoVerifyException(
                    f"Required signature was not found on {self.remote_manifest_url}"
                )
            return json.loads(manifest_contents)

    def read_manifest(
        self, manifest_url: Optional[str] = None, verify_signature: bool = True
    ) -> BuildcacheManifest:
        """Read and process the the buildcache entry manifest.

        If no manifest url is provided, build the url from the internal spec and
        base push url."""

        if self.manifest:
            if not manifest_url or manifest_url == self.remote_manifest_url:
                # We already have a manifest, so now calling this method without a specific
                # manifiest url, or with the same one we have internally, then skip reading
                # again, and just return the manifest we already read.
                return self.manifest

        self.manifest = None

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
            raise BuildcacheEntryError(f"Error reading manifest at {manifest_url}") from e

        if not manifest_contents:
            raise BuildcacheEntryError("Unable to read manifest or manifest empty")

        manifest_contents = self._maybe_verify_and_extract(
            manifest_contents, verify=verify_signature
        )

        self.manifest = BuildcacheManifest.from_json(manifest_contents)

        if self.manifest.version != 3:
            raise BuildcacheEntryError("Layout version mismatch in fetched manifest")

        return self.manifest

    def fetch_metadata(self, allow_unsigned: bool = False) -> dict:
        """Retrieve metadata for the spec, returns the validated spec dict"""
        if not self.manifest:
            # Reading the manifest will either successfully compute the remote
            # spec url, or else raise an exception
            self.read_manifest(verify_signature=not allow_unsigned)

        local_specfile_path = self.fetch_blob(self.get_blob_record(BuildcacheComponent.SPEC))

        # Check spec file for validity and read it, or else cleanup and exit early
        try:
            spec_dict, _ = get_valid_spec_file(local_specfile_path, self.get_layout_version())
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        return spec_dict

    def fetch_archive(self, allow_unsigned: bool = False) -> str:
        """Retrieve the archive file and return the local archive file path"""
        if not self.manifest:
            # Raises if problems encountered, including not being able to verify signagure
            self.read_manifest(verify_signature=not allow_unsigned)

        return self.fetch_blob(self.get_blob_record(BuildcacheComponent.TARBALL))

    def get_archive_stage(self) -> Optional[spack.stage.Stage]:
        return self.stages[self.get_blob_record(BuildcacheComponent.TARBALL)]
        # try:
        #     return self.stages[self.get_blob_record(BuildcacheComponent.TARBALL)]
        # except Exception as e:
        #     return None

    def fetch_index(self, allow_unsigned: bool = False) -> str:
        """Retrieve the buildcache index and return the path to the locally staged file"""
        if not self.manifest:
            # Raises if problems encountered, including not being able to verify signagure
            self.read_manifest(verify_signature=not allow_unsigned)

        return self.fetch_blob(self.get_blob_record(BuildcacheComponent.INDEX))

    def push(
        self,
        spec: spack.spec.Spec,
        tarball_path: str,
        checksum_algorithm: str,
        tarball_checksum: str,
        tmpdir: str,
        signing_key: Optional[str],
    ) -> None:
        """Push tarball, specfile, and manifest to the remote mirror

        Pushing should only be done after checking for the pre-existence of a
        buildcache entry for this spec, and represents a force push if one is
        found.  Thus, any pre-existing files are first removed.
        """

        spec_dict = spec.to_dict(hash=ht.dag_hash)
        layout_version = self.get_layout_version()
        spec_dict["buildcache_layout_version"] = layout_version
        tarball_content_length = os.stat(tarball_path).st_size
        compression = "gzip"

        if self.manifest:
            web_util.remove_url(self.remote_manifest_url)
            web_util.remove_url(
                self.get_blob_url(self.get_blob_record(BuildcacheComponent.TARBALL))
            )
            web_util.remove_url(self.get_blob_url(self.get_blob_record(BuildcacheComponent.SPEC)))
            self.manifest = None

        if not self.remote_manifest_url:
            self.remote_manifest_url = self.get_manifest_url(spec, self.mirror_url)

        # Any previous archive/tarball is gone, compute the path to the new one
        remote_archive_url = url_util.join(
            self.mirror_url,
            *self.get_relative_path_components(BuildcacheComponent.BLOBS),
            checksum_algorithm,
            tarball_checksum[:2],
            tarball_checksum,
        )

        # push the archive/tarball blob to the remote
        web_util.push_to_url(tarball_path, remote_archive_url, keep_original=False)

        # Clear out the previous data, then add a record for the new blob
        blobs: List[BlobRecord] = []
        blobs.append(
            BlobRecord(
                tarball_content_length,
                "tarball-v1",
                compression,
                checksum_algorithm,
                tarball_checksum,
            )
        )

        # compress the spec dict and compute its checksum
        specfile = os.path.join(tmpdir, f"{spec.dag_hash()}.spec.json")
        metadata_checksum, metadata_size = compress_and_write_spec(
            specfile, spec_dict, checksum_algorithm
        )

        # Any previous metadata blob is gone, compute the path to the new one
        remote_spec_url = url_util.join(
            self.mirror_url,
            *self.get_relative_path_components(BuildcacheComponent.BLOBS),
            checksum_algorithm,
            metadata_checksum[:2],
            metadata_checksum,
        )

        # push the metadata/spec blob to the remote
        web_util.push_to_url(specfile, remote_spec_url, keep_original=False)

        blobs.append(
            BlobRecord(
                metadata_size, "spec-v6", compression, checksum_algorithm, metadata_checksum
            )
        )

        # generate the manifest
        manifest = {
            "version": self.get_layout_version(),
            "data": [record.to_json() for record in blobs],
        }

        # write the manifest to a temporary location
        manifest_path = os.path.join(tmpdir, f"{spec.dag_hash()}.manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f)

        # possibly sign the manifest
        if signing_key:
            manifest_path = sign_specfile(signing_key, manifest_path)

        # Push the manifest file to the remote. The remote manifest url for
        # a given concrete spec is fixed, so we don't have to recompute it,
        # even if we deleted the pre-existing one.
        web_util.push_to_url(manifest_path, self.remote_manifest_url, keep_original=False)

    def destroy(self):
        """Destroy any existing stages"""
        for blob_stage in self.stages.values():
            blob_stage.destroy()

        self.stages = {}


class URLBuildcacheEntryV2(URLBuildcacheEntry):
    SPEC_URL_REGEX = re.compile(r"(.+)/build_cache/.+")
    LAYOUT_VERSION = 2
    # Uses the same SPEC_VERSION and TARBALL_VERSION as v3
    COMPONENT_PATHS = {
        BuildcacheComponent.BLOBS: ["build_cache"],
        BuildcacheComponent.INDICES: ["build_cache"],
        BuildcacheComponent.INDEX: ["build_cache", INDEX_JSON_FILE],
        BuildcacheComponent.INDEX_HASH: ["build_cache", INDEX_HASH_FILE],
        BuildcacheComponent.KEYS: ["build_cache", "keys", "_pgp"],
        BuildcacheComponent.SPECS: ["build_cache"],
    }

    def __init__(self, push_url_base: str, spec: Optional[spack.spec.Spec] = None):
        """Lazily initialize the object"""
        self.mirror_url: str = push_url_base
        self.spec: Optional[spack.spec.Spec] = spec

        self.has_metadata: bool = False
        self.has_tarball: bool = False
        self.has_signed: bool = False
        self.has_unsigned: bool = False
        self.spec_stage: Optional[spack.stage.Stage] = None
        self.local_specfile_path: str = ""
        self.archive_stage: Optional[spack.stage.Stage] = None
        self.local_archive_path: str = ""

        self.remote_spec_url: str = ""
        self.remote_archive_url: str = ""
        self.remote_archive_checksum_algorithm: str = ""
        self.remote_archive_checksum_hash: str = ""
        self.spec_dict: Dict[Any, Any] = {}

        self._checked_signed = False
        self._checked_unsigned = False
        self._checked_exists = False

    @classmethod
    def get_layout_version(cls) -> int:
        return cls.LAYOUT_VERSION

    def _get_spec_url(
        self, spec: spack.spec.Spec, mirror_url: str, ext: str = ".spec.json.sig"
    ) -> str:
        spec_formatted = spec.format_path(
            "{architecture}-{compiler.name}-{compiler.version}-{name}-{version}-{hash}"
        )
        path_components = self.get_relative_path_components(BuildcacheComponent.SPECS)
        return url_util.join(mirror_url, *path_components, f"{spec_formatted}{ext}")

    def _get_tarball_url(self, spec: spack.spec.Spec, mirror_url: str) -> str:
        directory_name = spec.format_path(
            "{architecture}/{compiler.name}-{compiler.version}/{name}-{version}"
        )
        spec_formatted = spec.format_path(
            "{architecture}-{compiler.name}-{compiler.version}-{name}-{version}-{hash}"
        )
        filename = f"{spec_formatted}.spack"
        return url_util.join(
            mirror_url,
            *self.get_relative_path_components(BuildcacheComponent.BLOBS),
            directory_name,
            filename,
        )

    def _check_metadata_exists(self):
        if not self.spec:
            return

        if not self._checked_signed:
            signed_url = self._get_spec_url(self.spec, self.mirror_url, ext=".spec.json.sig")
            if web_util.url_exists(signed_url):
                self.remote_spec_url = signed_url
                self.has_signed = True
            self._checked_signed = True

        if not self.has_signed and not self._checked_unsigned:
            unsigned_url = self._get_spec_url(self.spec, self.mirror_url, ext=".spec.json")
            if web_util.url_exists(unsigned_url):
                self.remote_spec_url = unsigned_url
                self.has_unsigned = True
            self._checked_unsigned = True

    def exists(self, components: List[BuildcacheComponent]) -> bool:
        if not self.spec:
            return False

        if (
            len(components) != 2
            or BuildcacheComponent.SPEC not in components
            or BuildcacheComponent.TARBALL not in components
        ):
            return False

        self._check_metadata_exists()
        if not self.has_signed and not self.has_unsigned:
            return False

        if not web_util.url_exists(self._get_tarball_url(self.spec, self.mirror_url)):
            return False

        return True

    def fetch_metadata(self, allow_unsigned: bool = False) -> dict:
        """Retrieve the v2 specfile for the spec, yields the validated spec+ dict"""
        if self.spec_dict:
            # Only fetch the metadata once
            return self.spec_dict

        self._check_metadata_exists()

        if not self.remote_spec_url:
            raise BuildcacheEntryError(f"Mirror {self.mirror_url} does not have metadata for spec")

        if not allow_unsigned and self.has_unsigned:
            raise BuildcacheEntryError(
                f"Mirror {self.mirror_url} does not have signed metadata for spec"
            )

        self.spec_stage = spack.stage.Stage(self.remote_spec_url)

        # Fetch the spec file, or else cleanup and exit early
        try:
            self.spec_stage.create()
            self.spec_stage.fetch()
        except spack.error.FetchError as e:
            self.destroy()
            raise BuildcacheEntryError(
                f"Unable to fetch metadata from {self.remote_spec_url}"
            ) from e

        self.local_specfile_path = self.spec_stage.save_filename

        if not allow_unsigned and not try_verify(self.local_specfile_path):
            raise NoVerifyException(f"Signature on {self.remote_spec_url} could not be verified")

        # Check spec file for validity and read it, or else cleanup and exit early
        try:
            spec_dict, _ = get_valid_spec_file(self.local_specfile_path, self.get_layout_version())
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        try:
            self.spec = spack.spec.Spec.from_dict(spec_dict)
        except Exception as err:
            raise BuildcacheEntryError("Fetched spec dict does not contain valid spec") from err

        self.spec_dict = spec_dict

        # Retrieve the alg and hash from the spec dict, use them to build the path to
        # the tarball.
        if "binary_cache_checksum" not in self.spec_dict:
            raise BuildcacheEntryError("Provided spec dict must contain 'binary_cache_checksum'")

        bchecksum = self.spec_dict["binary_cache_checksum"]

        if "hash_algorithm" not in bchecksum or "hash" not in bchecksum:
            raise BuildcacheEntryError(
                "Provided spec dict contains invalid 'binary_cache_checksum'"
            )

        self.remote_archive_checksum_algorithm = bchecksum["hash_algorithm"]
        self.remote_archive_checksum_hash = bchecksum["hash"]
        self.remote_archive_url = self._get_tarball_url(self.spec, self.mirror_url)

        return self.spec_dict

    def fetch_archive(self, allow_unsigned: bool = False) -> str:
        self.fetch_metadata(allow_unsigned=allow_unsigned)

        self.archive_stage = spack.stage.Stage(self.remote_archive_url)

        # Fetch the archive file, or else cleanup and exit early
        try:
            self.archive_stage.create()
            self.archive_stage.fetch()
        except spack.error.FetchError as e:
            self.destroy()
            raise BuildcacheEntryError(
                f"Unable to fetch archive from {self.remote_archive_url}"
            ) from e

        self.local_archive_path = self.archive_stage.save_filename

        # Raises if checksum does not match expected
        validate_checksum(
            self.local_archive_path,
            self.remote_archive_checksum_algorithm,
            self.remote_archive_checksum_hash,
        )

        return self.local_archive_path

    def get_archive_stage(self) -> Optional[spack.stage.Stage]:
        return self.archive_stage

    @classmethod
    def get_manifest_filename(cls, spec: spack.spec.Spec) -> str:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

    @classmethod
    def get_manifest_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest url")

    def read_manifest(
        self, manifest_url: Optional[str] = None, verify_signature: bool = True
    ) -> BuildcacheManifest:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

    def push(
        self,
        spec: spack.spec.Spec,
        tarball_path: str,
        checksum_algorithm: str,
        tarball_checksum: str,
        tmpdir: str,
        signing_key: Optional[str],
    ) -> None:
        raise BuildcacheEntryError("Spack can no longer push v2 buildcache entries")

    def destroy(self):
        if self.archive_stage:
            self.archive_stage.destroy()
            self.archive_stage = None
        if self.spec_stage:
            self.spec_stage.destroy()
            self.spec_stage = None


def get_url_buildcache_class(layout_version: int) -> type[URLBuildcacheEntry]:
    if layout_version == 2:
        return URLBuildcacheEntryV2
    elif layout_version == 3:
        return URLBuildcacheEntry
    else:
        raise UnknownBuildcacheLayoutError(
            f"Cannot create buildcache class for unknown layout version {layout_version}"
        )


def validate_checksum(file_path, checksum_algorithm, expected_checksum) -> None:
    """Compute the checksum of the given file and raise if invalid"""
    local_checksum = spack.util.crypto.checksum(
        spack.util.crypto.hash_fun_for_algo(checksum_algorithm), file_path
    )

    if local_checksum != expected_checksum:
        size, contents = fsys.filesummary(file_path)
        raise spack.error.NoChecksumException(
            file_path, size, contents, checksum_algorithm, expected_checksum, local_checksum
        )


def compress_and_write_spec(
    output_path: str, spec_dict: dict, checksum_algo: str
) -> Tuple[str, int]:
    """Compress the spec dict and write it to the given path

    Return the checksum (using the given algorithm) and size on disk of the file
    """
    # compress the spec dict and compute its checksum
    metadata_checksum = ""
    with open(output_path, "wb") as f:
        compressed_bytes = gzip.compress(
            json.dumps(spec_dict).encode("utf-8"), compresslevel=6, mtime=0
        )
        f.write(compressed_bytes)
        hasher = spack.util.crypto.hash_fun_for_algo(checksum_algo)()
        hasher.update(compressed_bytes)
        metadata_checksum = hasher.hexdigest()

    metadata_size = os.stat(output_path).st_size

    return (metadata_checksum, metadata_size)


def get_valid_spec_file(path: str, max_supported_layout: int) -> Tuple[Dict, int]:
    """Read and validate a spec file, returning the spec dict with its layout version, or raising
    InvalidMetadataFile if invalid."""
    try:
        with open(path, "rb") as f:
            binary_content = f.read()
    except OSError:
        raise InvalidMetadataFile(f"No such file: {path}")

    # Decompress spec file if necessary
    if binary_content[:2] == b"\x1f\x8b":
        binary_content = gzip.decompress(binary_content)

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


class NoSuchBlobException(spack.error.SpackError):
    """Raised when manifest does have some requested type of requested type"""

    pass


class NoVerifyException(BuildcacheEntryError):
    """
    Raised if file fails signature verification.
    """

    pass


class UnknownBuildcacheLayoutError(BuildcacheEntryError):
    """Raised when unrecognized buildcache layout version is encountered"""

    pass
