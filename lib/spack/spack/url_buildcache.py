# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import enum
import fnmatch
import gzip
import io
import json
import os
import re
import shutil
from contextlib import closing, contextmanager
from tempfile import TemporaryDirectory
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

import _vendoring.jsonschema

import llnl.util.filesystem as fsys
import llnl.util.tty as tty

import spack.config as config
import spack.database
import spack.error
import spack.hash_types as ht
import spack.mirrors.mirror
import spack.spec
import spack.stage
import spack.util.crypto
import spack.util.gpg
import spack.util.url as url_util
import spack.util.web as web_util
from spack.schema.url_buildcache_manifest import schema as buildcache_manifest_schema
from spack.util.archive import ChecksumWriter
from spack.util.crypto import hash_fun_for_algo
from spack.util.executable import which

#: The build cache layout version that this version of Spack creates.
#: Version 3: Introduces content-addressable tarballs
CURRENT_BUILD_CACHE_LAYOUT_VERSION = 3

#: The layout version spack can current install
SUPPORTED_LAYOUT_VERSIONS = (3, 2)

#: The name of the default buildcache index manifest file
INDEX_MANIFEST_FILE = "index.manifest.json"


class BuildcacheComponent(enum.Enum):
    """Enumeration of the kinds of things that live in a URL buildcache

    These enums serve two purposes: They allow different buildcache layout
    versions to specify different relative location of these entities, and
    they're used to map buildcache objects to their respective media types.
    """

    # metadata file for a binary package
    SPEC = enum.auto()
    # things that live in the blobs directory
    BLOB = enum.auto()
    # binary mirror index
    INDEX = enum.auto()
    # public key used for verifying signed binary packages
    KEY = enum.auto()
    # index of all public keys found in the mirror
    KEY_INDEX = enum.auto()
    # compressed archive of spec installation directory
    TARBALL = enum.auto()
    # binary mirror descriptor file
    LAYOUT_JSON = enum.auto()


class BlobRecord:
    """Class to describe a single data element (blob) from a manifest"""

    def __init__(
        self,
        content_length: int,
        media_type: str,
        compression_alg: str,
        checksum_alg: str,
        checksum: str,
    ) -> None:
        self.content_length = content_length
        self.media_type = media_type
        self.compression_alg = compression_alg
        self.checksum_alg = checksum_alg
        self.checksum = checksum

    @classmethod
    def from_dict(cls, record_dict):
        return BlobRecord(
            record_dict["contentLength"],
            record_dict["mediaType"],
            record_dict["compression"],
            record_dict["checksumAlgorithm"],
            record_dict["checksum"],
        )

    def to_dict(self):
        return {
            "contentLength": self.content_length,
            "mediaType": self.media_type,
            "compression": self.compression_alg,
            "checksumAlgorithm": self.checksum_alg,
            "checksum": self.checksum,
        }


class BuildcacheManifest:
    """A class to represent a buildcache manifest, which consists of a version
    number and an array of data blobs, each of which is represented by a
    BlobRecord."""

    def __init__(self, layout_version: int, data: Optional[List[BlobRecord]] = None):
        self.version: int = layout_version
        if data:
            self.data: List[BlobRecord] = [
                BlobRecord(
                    rec.content_length,
                    rec.media_type,
                    rec.compression_alg,
                    rec.checksum_alg,
                    rec.checksum,
                )
                for rec in data
            ]
        else:
            self.data = []

    def to_dict(self):
        return {"version": self.version, "data": [rec.to_dict() for rec in self.data]}

    @classmethod
    def from_dict(cls, manifest_json: Dict[str, Any]) -> "BuildcacheManifest":
        _vendoring.jsonschema.validate(manifest_json, buildcache_manifest_schema)
        return BuildcacheManifest(
            layout_version=manifest_json["version"],
            data=[BlobRecord.from_dict(blob_json) for blob_json in manifest_json["data"]],
        )

    def get_blob_records(self, media_type: str) -> List[BlobRecord]:
        """Return any blob records from the manifest matching the given media type"""
        matches: List[BlobRecord] = []

        for record in self.data:
            if record.media_type == media_type:
                matches.append(record)

        if matches:
            return matches

        raise NoSuchBlobException(f"Manifest has no blobs of type {media_type}")


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

    This class also provides generic manifest and blob management api, and it
    can be used to fetch and push other kinds of buildcache entries aside from
    just binary packages.  It can be used to work with public keys, buildcache
    indices, and any other type of data represented as a manifest which refers
    to blobs of data.

    """

    SPEC_URL_REGEX = re.compile(r"(.+)/v([\d]+)/manifests/.+")
    LAYOUT_VERSION = 3
    BUILDCACHE_INDEX_MEDIATYPE = f"application/vnd.spack.db.v{spack.database._DB_VERSION}+json"
    SPEC_MEDIATYPE = f"application/vnd.spack.spec.v{spack.spec.SPECFILE_FORMAT_VERSION}+json"
    TARBALL_MEDIATYPE = "application/vnd.spack.install.v2.tar+gzip"
    PUBLIC_KEY_MEDIATYPE = "application/pgp-keys"
    PUBLIC_KEY_INDEX_MEDIATYPE = "application/vnd.spack.keyindex.v1+json"
    BUILDCACHE_INDEX_FILE = "index.manifest.json"
    COMPONENT_PATHS = {
        BuildcacheComponent.BLOB: ["blobs"],
        BuildcacheComponent.INDEX: [f"v{LAYOUT_VERSION}", "manifests", "index"],
        BuildcacheComponent.KEY: [f"v{LAYOUT_VERSION}", "manifests", "key"],
        BuildcacheComponent.SPEC: [f"v{LAYOUT_VERSION}", "manifests", "spec"],
        BuildcacheComponent.KEY_INDEX: [f"v{LAYOUT_VERSION}", "manifests", "key"],
        BuildcacheComponent.TARBALL: ["blobs"],
        BuildcacheComponent.LAYOUT_JSON: [f"v{LAYOUT_VERSION}", "layout.json"],
    }

    def __init__(
        self, mirror_url: str, spec: Optional[spack.spec.Spec] = None, allow_unsigned: bool = False
    ):
        """Lazily initialize the object"""
        self.mirror_url: str = mirror_url
        self.spec: Optional[spack.spec.Spec] = spec
        self.allow_unsigned: bool = allow_unsigned
        self.manifest: Optional[BuildcacheManifest] = None
        self.remote_manifest_url: str = ""
        self.stages: Dict[BlobRecord, spack.stage.Stage] = {}

    @classmethod
    def get_layout_version(cls) -> int:
        """Returns the layout version of this class"""
        return cls.LAYOUT_VERSION

    @classmethod
    def check_layout_json_exists(cls, mirror_url: str) -> bool:
        """Return True if layout.json exists in the expected location, False otherwise"""
        layout_json_url = url_util.join(
            mirror_url, *cls.get_relative_path_components(BuildcacheComponent.LAYOUT_JSON)
        )
        return web_util.url_exists(layout_json_url)

    @classmethod
    def maybe_push_layout_json(cls, mirror_url: str) -> None:
        """This function does nothing if layout.json already exists, otherwise it
        pushes layout.json to the expected location in the mirror"""
        if cls.check_layout_json_exists(mirror_url):
            return

        layout_contents = {"signing": "gpg"}

        with TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
            local_layout_path = os.path.join(tmpdir, "layout.json")
            with open(local_layout_path, "w", encoding="utf-8") as fd:
                json.dump(layout_contents, fd)
            remote_layout_url = url_util.join(
                mirror_url, *cls.get_relative_path_components(BuildcacheComponent.LAYOUT_JSON)
            )
            web_util.push_to_url(local_layout_path, remote_layout_url, keep_original=False)

    @classmethod
    def get_base_url(cls, manifest_url: str) -> str:
        """Given any manifest url (i.e. one containing 'v3/manifests/') return the
        base part of the url"""
        rematch = cls.SPEC_URL_REGEX.match(manifest_url)
        if not rematch:
            raise BuildcacheEntryError(f"Unable to parse spec url: {manifest_url}")
        return rematch.group(1)

    @classmethod
    def get_index_url(cls, mirror_url: str):
        return url_util.join(
            mirror_url,
            *cls.get_relative_path_components(BuildcacheComponent.INDEX),
            cls.BUILDCACHE_INDEX_FILE,
        )

    @classmethod
    def get_relative_path_components(cls, component: BuildcacheComponent) -> List[str]:
        """Given any type of buildcache component, return its relative location within
        a mirror as a list path elements"""
        return cls.COMPONENT_PATHS[component]

    @classmethod
    def get_manifest_filename(cls, spec: spack.spec.Spec) -> str:
        """Given a concrete spec, compute and return the name (i.e. basename) of
        the manifest file representing it"""
        spec_formatted = spec.format_path("{name}-{version}-{hash}")
        return f"{spec_formatted}.spec.manifest.json"

    @classmethod
    def get_manifest_url(cls, spec: spack.spec.Spec, mirror_url: str) -> str:
        """Given a concrete spec and a base url, return the full url where the
        spec manifest should be found"""
        path_components = cls.get_relative_path_components(BuildcacheComponent.SPEC)
        return url_util.join(
            mirror_url, *path_components, spec.name, cls.get_manifest_filename(spec)
        )

    @classmethod
    def get_buildcache_component_include_pattern(
        cls, buildcache_component: Optional[BuildcacheComponent] = None
    ) -> str:
        """Given a buildcache component, return the glob pattern that can be used
        to match it in a directory listing.  If None is provided, return a catch-all
        pattern that will match all buildcache components."""
        if buildcache_component is None:
            return "*.manifest.json"
        elif buildcache_component == BuildcacheComponent.SPEC:
            return "*.spec.manifest.json"
        elif buildcache_component == BuildcacheComponent.INDEX:
            return ".*index.manifest.json"
        elif buildcache_component == BuildcacheComponent.KEY:
            return "*.key.manifest.json"
        elif buildcache_component == BuildcacheComponent.KEY_INDEX:
            return "keys.manifest.json"

        raise BuildcacheEntryError(f"Not a manifest component: {buildcache_component}")

    @classmethod
    def component_to_media_type(cls, component: BuildcacheComponent) -> str:
        """Mapping from buildcache component to media type"""
        if component == BuildcacheComponent.SPEC:
            return cls.SPEC_MEDIATYPE
        elif component == BuildcacheComponent.TARBALL:
            return cls.TARBALL_MEDIATYPE
        elif component == BuildcacheComponent.INDEX:
            return cls.BUILDCACHE_INDEX_MEDIATYPE
        elif component == BuildcacheComponent.KEY:
            return cls.PUBLIC_KEY_MEDIATYPE
        elif component == BuildcacheComponent.KEY_INDEX:
            return cls.PUBLIC_KEY_INDEX_MEDIATYPE

        raise BuildcacheEntryError(f"Not a blob component: {component}")

    def get_local_spec_path(self) -> str:
        """Convenience method to return the local path of a fetched spec file"""
        return self.get_staged_blob_path(self.get_blob_record(BuildcacheComponent.SPEC))

    def get_local_archive_path(self) -> str:
        """Convenience method to return the local path of a fetched tarball"""
        return self.get_staged_blob_path(self.get_blob_record(BuildcacheComponent.TARBALL))

    def get_blob_record(self, blob_type: BuildcacheComponent) -> BlobRecord:
        """Return the first blob record of the given type. Assumes the manifest has
        already been fetched."""
        if not self.manifest:
            raise BuildcacheEntryError("Read manifest before accessing blob records")

        records = self.manifest.get_blob_records(self.component_to_media_type(blob_type))

        if len(records) == 0:
            raise BuildcacheEntryError(f"Manifest has no blob record of type {blob_type}")

        return records[0]

    def check_blob_exists(self, record: BlobRecord) -> bool:
        """Return True if the blob given by record exists on the mirror, False otherwise"""
        blob_url = self.get_blob_url(self.mirror_url, record)
        return web_util.url_exists(blob_url)

    @classmethod
    def get_blob_path_components(cls, record: BlobRecord) -> List[str]:
        """Given a BlobRecord, return the relative path of the blob within a mirror
        as a list of path components"""
        return [
            *cls.get_relative_path_components(BuildcacheComponent.BLOB),
            record.checksum_alg,
            record.checksum[:2],
            record.checksum,
        ]

    @classmethod
    def get_blob_url(cls, mirror_url: str, record: BlobRecord) -> str:
        """Return the full url of the blob given by record"""
        return url_util.join(mirror_url, *cls.get_blob_path_components(record))

    def fetch_blob(self, record: BlobRecord) -> str:
        """Given a blob record, find associated blob in the manifest and stage it

        Returns the local path to the staged blob
        """
        if record not in self.stages:
            blob_url = self.get_blob_url(self.mirror_url, record)
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
        """Convenience method to return the local path of a staged blob"""
        if record not in self.stages:
            raise BuildcacheEntryError(f"Blob not staged: {record}")

        return self.stages[record].save_filename

    def exists(self, components: List[BuildcacheComponent]) -> bool:
        """Check whether blobs exist for all specified components

        Returns True if there is a blob present in the mirror for every
        given component type.
        """
        try:
            self.read_manifest()
        except BuildcacheEntryError:
            return False

        if not self.manifest:
            return False

        for component in components:
            component_blobs = self.manifest.get_blob_records(
                self.component_to_media_type(component)
            )

            if len(component_blobs) == 0:
                return False

            if not self.check_blob_exists(component_blobs[0]):
                return False

        return True

    @classmethod
    def verify_and_extract_manifest(cls, manifest_contents: str, verify: bool = False) -> dict:
        """Possibly verify clearsig, then extract contents and return as json"""
        magic_string = "-----BEGIN PGP SIGNED MESSAGE-----"
        if manifest_contents.startswith(magic_string):
            if verify:
                # Rry to verify and raise if we fail
                with TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
                    manifest_path = os.path.join(tmpdir, "manifest.json.sig")
                    with open(manifest_path, "w", encoding="utf-8") as fd:
                        fd.write(manifest_contents)
                    if not try_verify(manifest_path):
                        raise NoVerifyException("Signature could not be verified")

            return spack.spec.Spec.extract_json_from_clearsig(manifest_contents)
        else:
            if verify:
                raise NoVerifyException("Required signature was not found on manifest")
            return json.loads(manifest_contents)

    def read_manifest(self, manifest_url: Optional[str] = None) -> BuildcacheManifest:
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

        manifest_contents = self.verify_and_extract_manifest(
            manifest_contents, verify=not self.allow_unsigned
        )

        self.manifest = BuildcacheManifest.from_dict(manifest_contents)

        if self.manifest.version != 3:
            raise BuildcacheEntryError("Layout version mismatch in fetched manifest")

        return self.manifest

    def fetch_metadata(self) -> dict:
        """Retrieve metadata for the spec, returns the validated spec dict"""
        if not self.manifest:
            # Reading the manifest will either successfully compute the remote
            # spec url, or else raise an exception
            self.read_manifest()

        local_specfile_path = self.fetch_blob(self.get_blob_record(BuildcacheComponent.SPEC))

        # Check spec file for validity and read it, or else cleanup and exit early
        try:
            spec_dict, _ = get_valid_spec_file(local_specfile_path, self.get_layout_version())
        except InvalidMetadataFile as e:
            self.destroy()
            raise BuildcacheEntryError("Buildcache entry does not have valid metadata file") from e

        return spec_dict

    def fetch_archive(self) -> str:
        """Retrieve the archive file and return the local archive file path"""
        if not self.manifest:
            # Raises if problems encountered, including not being able to verify signagure
            self.read_manifest()

        return self.fetch_blob(self.get_blob_record(BuildcacheComponent.TARBALL))

    def get_archive_stage(self) -> Optional[spack.stage.Stage]:
        return self.stages[self.get_blob_record(BuildcacheComponent.TARBALL)]

    def remove(self):
        """Remove a binary package (spec file and tarball) and the associated
        manifest from the mirror."""
        if self.manifest:
            try:
                web_util.remove_url(self.remote_manifest_url)
            except Exception as e:
                tty.debug(f"Failed to remove previous manfifest: {e}")

            try:
                web_util.remove_url(
                    self.get_blob_url(
                        self.mirror_url, self.get_blob_record(BuildcacheComponent.TARBALL)
                    )
                )
            except Exception as e:
                tty.debug(f"Failed to remove previous archive: {e}")

            try:
                web_util.remove_url(
                    self.get_blob_url(
                        self.mirror_url, self.get_blob_record(BuildcacheComponent.SPEC)
                    )
                )
            except Exception as e:
                tty.debug(f"Failed to remove previous metadata: {e}")

            self.manifest = None

    @classmethod
    def push_blob(cls, mirror_url: str, blob_path: str, record: BlobRecord) -> None:
        """Push the blob_path file to mirror as a blob represented by the given
        record"""
        blob_destination_url = cls.get_blob_url(mirror_url, record)
        web_util.push_to_url(blob_path, blob_destination_url, keep_original=False)

    @classmethod
    def push_manifest(
        cls,
        mirror_url: str,
        manifest_name: str,
        manifest: BuildcacheManifest,
        tmpdir: str,
        component_type: BuildcacheComponent = BuildcacheComponent.SPEC,
        signing_key: Optional[str] = None,
    ) -> None:
        """Given a BuildcacheManifest, push it to the mirror using the given manifest
        name.  The component_type is used to indicate what type of thing the manifest
        represents, so it can be placed in the correct relative path within the mirror.
        If a signing_key is provided, it will be used to clearsign the manifest before
        pushing it."""
        # write the manifest to a temporary location
        manifest_file_name = f"{manifest_name}.manifest.json"
        manifest_path = os.path.join(tmpdir, manifest_file_name)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=0, separators=(",", ":"))
            # Note: when using gpg clear sign, we need to avoid long lines (19995
            # chars). If lines are longer, they are truncated without error. So,
            # here we still add newlines, but no indent, so save on file size and
            # line length.

        if signing_key:
            manifest_path = sign_file(signing_key, manifest_path)

        manifest_destination_url = url_util.join(
            mirror_url, *cls.get_relative_path_components(component_type), manifest_file_name
        )

        web_util.push_to_url(manifest_path, manifest_destination_url, keep_original=False)

    @classmethod
    def push_local_file_as_blob(
        cls,
        local_file_path: str,
        mirror_url: str,
        manifest_name: str,
        component_type: BuildcacheComponent,
        compression: str = "none",
    ) -> None:
        """Convenience method to push a local file to a mirror as a blob.  Both manifest
        and blob are pushed as a component of the given component_type.  If compression
        is 'gzip' the blob will be compressed before pushing, otherwise it will be pushed
        uncompressed."""
        cache_class = get_url_buildcache_class()
        checksum_algo = "sha256"
        blob_to_push = local_file_path

        with TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
            blob_to_push = os.path.join(tmpdir, os.path.basename(local_file_path))

            with compression_writer(blob_to_push, compression, checksum_algo) as (
                fout,
                checker,
            ), open(local_file_path, "rb") as fin:
                shutil.copyfileobj(fin, fout)

            record = BlobRecord(
                checker.length,
                cache_class.component_to_media_type(component_type),
                compression,
                checksum_algo,
                checker.hexdigest(),
            )
            manifest = BuildcacheManifest(
                layout_version=CURRENT_BUILD_CACHE_LAYOUT_VERSION, data=[record]
            )
            cls.push_blob(mirror_url, blob_to_push, record)
            cls.push_manifest(
                mirror_url, manifest_name, manifest, tmpdir, component_type=component_type
            )

    def push_binary_package(
        self,
        spec: spack.spec.Spec,
        tarball_path: str,
        checksum_algorithm: str,
        tarball_checksum: str,
        tmpdir: str,
        signing_key: Optional[str],
    ) -> None:
        """Convenience method to push tarball, specfile, and manifest to the remote mirror

        Pushing should only be done after checking for the pre-existence of a
        buildcache entry for this spec, and represents a force push if one is
        found.  Thus, any pre-existing files are first removed.
        """

        spec_dict = spec.to_dict(hash=ht.dag_hash)
        # TODO: Remove this key once oci buildcache no longer uses it
        spec_dict["buildcache_layout_version"] = 2
        tarball_content_length = os.stat(tarball_path).st_size
        compression = "gzip"

        # Delete the previously existing version
        self.remove()

        if not self.remote_manifest_url:
            self.remote_manifest_url = self.get_manifest_url(spec, self.mirror_url)

        # Any previous archive/tarball is gone, compute the path to the new one
        remote_archive_url = url_util.join(
            self.mirror_url,
            *self.get_relative_path_components(BuildcacheComponent.BLOB),
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
                self.TARBALL_MEDIATYPE,
                compression,
                checksum_algorithm,
                tarball_checksum,
            )
        )

        # compress the spec dict and compute its checksum
        specfile = os.path.join(tmpdir, f"{spec.dag_hash()}.spec.json")
        metadata_checksum, metadata_size = compressed_json_from_dict(
            specfile, spec_dict, checksum_algorithm
        )

        # Any previous metadata blob is gone, compute the path to the new one
        remote_spec_url = url_util.join(
            self.mirror_url,
            *self.get_relative_path_components(BuildcacheComponent.BLOB),
            checksum_algorithm,
            metadata_checksum[:2],
            metadata_checksum,
        )

        # push the metadata/spec blob to the remote
        web_util.push_to_url(specfile, remote_spec_url, keep_original=False)

        blobs.append(
            BlobRecord(
                metadata_size,
                self.SPEC_MEDIATYPE,
                compression,
                checksum_algorithm,
                metadata_checksum,
            )
        )

        # generate the manifest
        manifest = {
            "version": self.get_layout_version(),
            "data": [record.to_dict() for record in blobs],
        }

        # write the manifest to a temporary location
        manifest_path = os.path.join(tmpdir, f"{spec.dag_hash()}.manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=0, separators=(",", ":"))
            # Note: when using gpg clear sign, we need to avoid long lines (19995
            # chars). If lines are longer, they are truncated without error. So,
            # here we still add newlines, but no indent, so save on file size and
            # line length.

        # possibly sign the manifest
        if signing_key:
            manifest_path = sign_file(signing_key, manifest_path)

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
    """This class exists to provide read-only support for reading older buildcache
    layouts in a way that is transparent to binary_distribution code responsible for
    downloading and extracting binary packages.  Since support for layout v2 is
    read-only, and since v2 did not have support for manifests and blobs, many class
    and instance methods are overridden simply to raise, hopefully making the intended
    use and limitations of the class clear to developers."""

    SPEC_URL_REGEX = re.compile(r"(.+)/build_cache/.+")
    LAYOUT_VERSION = 2
    BUILDCACHE_INDEX_FILE = "index.json"
    COMPONENT_PATHS = {
        BuildcacheComponent.BLOB: ["build_cache"],
        BuildcacheComponent.INDEX: ["build_cache"],
        BuildcacheComponent.KEY: ["build_cache", "_pgp"],
        BuildcacheComponent.SPEC: ["build_cache"],
        BuildcacheComponent.KEY_INDEX: ["build_cache", "_pgp"],
        BuildcacheComponent.TARBALL: ["build_cache"],
        BuildcacheComponent.LAYOUT_JSON: ["build_cache", "layout.json"],
    }

    def __init__(
        self,
        push_url_base: str,
        spec: Optional[spack.spec.Spec] = None,
        allow_unsigned: bool = False,
    ):
        """Lazily initialize the object"""
        self.mirror_url: str = push_url_base
        self.spec: Optional[spack.spec.Spec] = spec
        self.allow_unsigned: bool = allow_unsigned

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

    @classmethod
    def maybe_push_layout_json(cls, mirror_url: str) -> None:
        raise BuildcacheEntryError("spack can no longer write to v2 buildcaches")

    def _get_spec_url(
        self, spec: spack.spec.Spec, mirror_url: str, ext: str = ".spec.json.sig"
    ) -> str:
        spec_formatted = spec.format_path(
            "{architecture}-{compiler.name}-{compiler.version}-{name}-{version}-{hash}"
        )
        path_components = self.get_relative_path_components(BuildcacheComponent.SPEC)
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
            *self.get_relative_path_components(BuildcacheComponent.BLOB),
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

    def fetch_metadata(self) -> dict:
        """Retrieve the v2 specfile for the spec, yields the validated spec+ dict"""
        if self.spec_dict:
            # Only fetch the metadata once
            return self.spec_dict

        self._check_metadata_exists()

        if not self.remote_spec_url:
            raise BuildcacheEntryError(f"Mirror {self.mirror_url} does not have metadata for spec")

        if not self.allow_unsigned and self.has_unsigned:
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

        if not self.allow_unsigned and not try_verify(self.local_specfile_path):
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

    def fetch_archive(self) -> str:
        self.fetch_metadata()

        # Adding this, we can avoid passing a dictionary of stages around the
        # install logic, and in fact completely avoid fetching the metadata in
        # the new (v3) approach.
        if self.spec_stage:
            self.spec_stage.destroy()
            self.spec_stage = None

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

    @classmethod
    def get_buildcache_component_include_pattern(
        cls, buildcache_component: Optional[BuildcacheComponent] = None
    ) -> str:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

    def read_manifest(self, manifest_url: Optional[str] = None) -> BuildcacheManifest:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

    def remove(self):
        raise BuildcacheEntryError("Spack cannot delete v2 buildcache entries")

    def get_blob_record(self, blob_type: BuildcacheComponent) -> BlobRecord:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    def check_blob_exists(self, record: BlobRecord) -> bool:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    @classmethod
    def get_blob_path_components(cls, record: BlobRecord) -> List[str]:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    @classmethod
    def get_blob_url(cls, mirror_url: str, record: BlobRecord) -> str:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    def fetch_blob(self, record: BlobRecord) -> str:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    def get_staged_blob_path(self, record: BlobRecord) -> str:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    @classmethod
    def verify_and_extract_manifest(cls, manifest_contents: str, verify: bool = False) -> dict:
        raise BuildcacheEntryError("v2 buildcache entries do not have a manifest file")

    @classmethod
    def push_blob(cls, mirror_url: str, blob_path: str, record: BlobRecord) -> None:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    @classmethod
    def push_manifest(
        cls,
        mirror_url: str,
        manifest_name: str,
        manifest: BuildcacheManifest,
        tmpdir: str,
        component_type: BuildcacheComponent = BuildcacheComponent.SPEC,
        signing_key: Optional[str] = None,
    ) -> None:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    @classmethod
    def push_local_file_as_blob(
        cls,
        local_file_path: str,
        mirror_url: str,
        manifest_name: str,
        component_type: BuildcacheComponent,
        compression: str = "none",
    ) -> None:
        raise BuildcacheEntryError("v2 buildcache layout is unaware of manifests and blobs")

    def push_binary_package(
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


def get_url_buildcache_class(
    layout_version: int = CURRENT_BUILD_CACHE_LAYOUT_VERSION,
) -> Type[URLBuildcacheEntry]:
    """Given a layout version, return the class responsible for managing access
    to buildcache entries of that version"""
    if layout_version == 2:
        return URLBuildcacheEntryV2
    elif layout_version == 3:
        return URLBuildcacheEntry
    else:
        raise UnknownBuildcacheLayoutError(
            f"Cannot create buildcache class for unknown layout version {layout_version}"
        )


def check_mirror_for_layout(mirror: spack.mirrors.mirror.Mirror):
    """Check specified mirror, and warn if missing layout.json"""
    cache_class = get_url_buildcache_class()
    if not cache_class.check_layout_json_exists(mirror.fetch_url):
        msg = (
            f"Configured mirror {mirror.name} is missing layout.json and has either \n"
            "    never been pushed or is of an old layout version. If it's the latter, \n"
            "    consider running 'spack buildcache migrate' or rebuilding the specs in \n"
            "    in this mirror."
        )
        tty.warn(msg)


def _entries_from_cache_aws_cli(
    url: str, tmpspecsdir: str, component_type: Optional[BuildcacheComponent] = None
):
    """Use aws cli to sync all manifests into a local temporary directory.

    Args:
        url: prefix of the build cache on s3
        tmpspecsdir: path to temporary directory to use for writing files
        component_type: type of buildcache component to sync (spec, index, key, etc.)

    Return:
        A tuple where the first item is a list of local file paths pointing
        to the manifests that should be read from the mirror, and the
        second item is a function taking a url or file path and returning
        a `URLBuildcacheEntry` for that manifest.
    """
    read_fn = None
    file_list = None
    aws = which("aws")

    cache_class = get_url_buildcache_class(layout_version=CURRENT_BUILD_CACHE_LAYOUT_VERSION)

    if not aws:
        tty.warn("Failed to use aws s3 sync to retrieve specs, falling back to parallel fetch")
        return file_list, read_fn

    def file_read_method(manifest_path: str) -> URLBuildcacheEntry:
        cache_entry = cache_class(mirror_url=url, allow_unsigned=True)
        cache_entry.read_manifest(manifest_url=f"file://{manifest_path}")
        return cache_entry

    include_pattern = cache_class.get_buildcache_component_include_pattern(component_type)

    sync_command_args = [
        "s3",
        "sync",
        "--exclude",
        "*",
        "--include",
        include_pattern,
        url,
        tmpspecsdir,
    ]

    tty.debug(f"Using aws s3 sync to download manifests from {url} to {tmpspecsdir}")

    try:
        aws(*sync_command_args, output=os.devnull, error=os.devnull)
        file_list = fsys.find(tmpspecsdir, [include_pattern])
        read_fn = file_read_method
    except Exception:
        tty.warn("Failed to use aws s3 sync to retrieve specs, falling back to parallel fetch")

    return file_list, read_fn


def _entries_from_cache_fallback(
    url: str, tmpspecsdir: str, component_type: Optional[BuildcacheComponent] = None
):
    """Use spack.util.web module to get a list of all the manifests at the remote url.

    Args:
        url: Base url of mirror (location of manifest files)
        tmpspecsdir: path to temporary directory to use for writing files
        component_type: type of buildcache component to sync (spec, index, key, etc.)

    Return:
        A tuple where the first item is a list of absolute file paths or
        urls pointing to the manifests that should be read from the mirror,
        and the second item is a function taking a url or file path of a manifest and
        returning a `URLBuildcacheEntry` for that manifest.
    """
    read_fn = None
    file_list = None

    cache_class = get_url_buildcache_class(layout_version=CURRENT_BUILD_CACHE_LAYOUT_VERSION)

    def url_read_method(manifest_url: str) -> URLBuildcacheEntry:
        cache_entry = cache_class(mirror_url=url, allow_unsigned=True)
        cache_entry.read_manifest(manifest_url)
        return cache_entry

    try:
        file_list = [
            url_util.join(url, entry)
            for entry in web_util.list_url(url, recursive=True)
            if fnmatch.fnmatch(
                entry, cache_class.get_buildcache_component_include_pattern(component_type)
            )
        ]
        read_fn = url_read_method
    except Exception as err:
        # If we got some kind of S3 (access denied or other connection error), the first non
        # boto-specific class in the exception is Exception.  Just print a warning and return
        tty.warn(f"Encountered problem listing packages at {url}: {err}")

    return file_list, read_fn


def get_entries_from_cache(
    url: str, tmpspecsdir: str, component_type: Optional[BuildcacheComponent] = None
):
    """Get a list of all the manifests in the mirror and a function to read them.

    Args:
        url: Base url of mirror (location of spec files)
        tmpspecsdir: Temporary location for writing files
        component_type: type of buildcache component to sync (spec, index, key, etc.)

    Return:
        A tuple where the first item is a list of absolute file paths or
        urls pointing to the manifests that should be read from the mirror,
        and the second item is a function taking a url or file path and
        returning a `URLBuildcacheEntry` for that manifest.
    """
    callbacks: List[Callable] = []
    if url.startswith("s3://"):
        callbacks.append(_entries_from_cache_aws_cli)

    callbacks.append(_entries_from_cache_fallback)

    for specs_from_cache_fn in callbacks:
        file_list, read_fn = specs_from_cache_fn(url, tmpspecsdir, component_type)
        if file_list:
            return file_list, read_fn

    raise ListMirrorSpecsError("Failed to get list of entries from {0}".format(url))


def validate_checksum(file_path, checksum_algorithm, expected_checksum) -> None:
    """Compute the checksum of the given file and raise if invalid"""
    local_checksum = spack.util.crypto.checksum(hash_fun_for_algo(checksum_algorithm), file_path)

    if local_checksum != expected_checksum:
        size, contents = fsys.filesummary(file_path)
        raise spack.error.NoChecksumException(
            file_path, size, contents, checksum_algorithm, expected_checksum, local_checksum
        )


def _get_compressor(compression: str, writable: io.BufferedIOBase) -> io.BufferedIOBase:
    if compression == "gzip":
        return gzip.GzipFile(filename="", mode="wb", compresslevel=6, mtime=0, fileobj=writable)
    elif compression == "none":
        return writable
    else:
        raise BuildcacheEntryError(f"Unknown compression type: {compression}")


@contextmanager
def compression_writer(output_path: str, compression: str, checksum_algo: str):
    """Create and return a writer capable of writing compressed data. Available
    options for compression are "gzip" or "none", checksum_algo is used to pick
    the checksum algorithm used by the ChecksumWriter.

    Yields a tuple containing:
        io.IOBase: writer that can compress (or not) as it writes
        ChecksumWriter: provides checksum and length of written data
    """
    with open(output_path, "wb") as writer, ChecksumWriter(
        fileobj=writer, algorithm=hash_fun_for_algo(checksum_algo)
    ) as checksum_writer, closing(
        _get_compressor(compression, checksum_writer)
    ) as compress_writer:
        yield compress_writer, checksum_writer


def compressed_json_from_dict(
    output_path: str, spec_dict: dict, checksum_algo: str
) -> Tuple[str, int]:
    """Compress the spec dict and write it to the given path

    Return the checksum (using the given algorithm) and size on disk of the file
    """
    with compression_writer(output_path, "gzip", checksum_algo) as (
        f_bin,
        checker,
    ), io.TextIOWrapper(f_bin, encoding="utf-8") as f_txt:
        json.dump(spec_dict, f_txt, separators=(",", ":"))

    return checker.hexdigest(), checker.length


def get_valid_spec_file(path: str, max_supported_layout: int) -> Tuple[Dict, int]:
    """Read and validate a spec file, returning the spec dict with its layout version, or raising
    InvalidMetadataFile if invalid."""
    try:
        with open(path, "rb") as f:
            binary_content = f.read()
    except OSError as e:
        raise InvalidMetadataFile(f"No such file: {path}") from e

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


def sign_file(key: str, file_path: str) -> str:
    """sign and return the path to the signed file"""
    signed_file_path = f"{file_path}.sig"
    spack.util.gpg.sign(key, file_path, signed_file_path, clearsign=True)
    return signed_file_path


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
    """Simple class to hold a mirror url and a buildcache layout version

    This class is used by BinaryCacheIndex to produce a key used to keep
    track of downloaded/processed buildcache index files from remote mirrors
    in some layout version."""

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
    """Simple holder for a mirror (represented by a url and a layout version) and
    an associated concrete spec"""

    url_and_version: MirrorURLAndVersion
    spec: spack.spec.Spec

    def __init__(self, url_and_version: MirrorURLAndVersion, spec: spack.spec.Spec):
        self.url_and_version = url_and_version
        self.spec = spec


class InvalidMetadataFile(spack.error.SpackError):
    """Raised when spack encounters a spec file it cannot understand or process"""

    pass


class BuildcacheEntryError(spack.error.SpackError):
    """Raised for problems finding or accessing binary cache entry on mirror"""

    pass


class NoSuchBlobException(spack.error.SpackError):
    """Raised when manifest does have some requested type of requested type"""

    pass


class NoVerifyException(BuildcacheEntryError):
    """Raised if file fails signature verification"""

    pass


class UnknownBuildcacheLayoutError(BuildcacheEntryError):
    """Raised when unrecognized buildcache layout version is encountered"""

    pass


class ListMirrorSpecsError(spack.error.SpackError):
    """Raised when unable to retrieve list of specs from the mirror"""
