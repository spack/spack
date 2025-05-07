# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import json
import os
import pathlib
import tempfile
from typing import NamedTuple

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.database as spack_db
import spack.error
import spack.mirrors.mirror
import spack.spec
import spack.stage
import spack.util.crypto
import spack.util.parallel
import spack.util.url as url_util
import spack.util.web as web_util

from .enums import InstallRecordStatus
from .url_buildcache import (
    BlobRecord,
    BuildcacheComponent,
    compressed_json_from_dict,
    get_url_buildcache_class,
    sign_file,
    try_verify,
)


def v2_tarball_directory_name(spec):
    """
    Return name of the tarball directory according to the convention
    <os>-<architecture>/<compiler>/<package>-<version>/
    """
    return spec.format_path("{architecture}/{compiler.name}-{compiler.version}/{name}-{version}")


def v2_tarball_name(spec, ext):
    """
    Return the name of the tarfile according to the convention
    <os>-<architecture>-<package>-<dag_hash><ext>
    """
    spec_formatted = spec.format_path(
        "{architecture}-{compiler.name}-{compiler.version}-{name}-{version}-{hash}"
    )
    return f"{spec_formatted}{ext}"


def v2_tarball_path_name(spec, ext):
    """
    Return the full path+name for a given spec according to the convention
    <tarball_directory_name>/<tarball_name>
    """
    return os.path.join(v2_tarball_directory_name(spec), v2_tarball_name(spec, ext))


class MigrateSpecResult(NamedTuple):
    success: bool
    message: str


class MigrationException(spack.error.SpackError):
    """
    Raised when migration fails irrevocably
    """

    def __init__(self, msg):
        super().__init__(msg)


def _migrate_spec(
    s: spack.spec.Spec, mirror_url: str, tmpdir: str, unsigned: bool = False, signing_key: str = ""
) -> MigrateSpecResult:
    """Parallelizable function to migrate a single spec"""
    print_spec = f"{s.name}/{s.dag_hash()[:7]}"

    # Check if the spec file exists in the new location and exit early if so

    v3_cache_class = get_url_buildcache_class(layout_version=3)
    v3_cache_entry = v3_cache_class(mirror_url, s, allow_unsigned=unsigned)
    exists = v3_cache_entry.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])
    v3_cache_entry.destroy()

    if exists:
        msg = f"No need to migrate {print_spec}"
        return MigrateSpecResult(True, msg)

    # Try to fetch the spec metadata
    v2_metadata_urls = [
        url_util.join(mirror_url, "build_cache", v2_tarball_name(s, ".spec.json.sig"))
    ]

    if unsigned:
        v2_metadata_urls.append(
            url_util.join(mirror_url, "build_cache", v2_tarball_name(s, ".spec.json"))
        )

    spec_contents = None

    for meta_url in v2_metadata_urls:
        try:
            _, _, meta_file = web_util.read_from_url(meta_url)
            spec_contents = codecs.getreader("utf-8")(meta_file).read()
            v2_spec_url = meta_url
            break
        except (web_util.SpackWebError, OSError):
            pass
    else:
        msg = f"Unable to read metadata for {print_spec}"
        return MigrateSpecResult(False, msg)

    spec_dict = {}

    if unsigned:
        # User asked for unsigned, if we found a signed specfile, just ignore
        # the signature
        if v2_spec_url.endswith(".sig"):
            spec_dict = spack.spec.Spec.extract_json_from_clearsig(spec_contents)
        else:
            spec_dict = json.loads(spec_contents)
    else:
        # User asked for signed, we must successfully verify the signature
        local_signed_pre_verify = os.path.join(
            tmpdir, f"{s.name}_{s.dag_hash()}_verify.spec.json.sig"
        )
        with open(local_signed_pre_verify, "w", encoding="utf-8") as fd:
            fd.write(spec_contents)
        if not try_verify(local_signed_pre_verify):
            return MigrateSpecResult(False, f"Failed to verify signature of {print_spec}")
        with open(local_signed_pre_verify, encoding="utf-8") as fd:
            spec_dict = spack.spec.Spec.extract_json_from_clearsig(fd.read())

    # Read out and remove the bits needed to rename and position the archive
    bcc = spec_dict.pop("binary_cache_checksum", None)
    if not bcc:
        msg = "Cannot migrate a spec that does not have 'binary_cache_checksum'"
        return MigrateSpecResult(False, msg)

    algorithm = bcc["hash_algorithm"]
    checksum = bcc["hash"]

    # TODO: Remove this key once oci buildcache no longer uses it
    spec_dict["buildcache_layout_version"] = 2

    v2_archive_url = url_util.join(mirror_url, "build_cache", v2_tarball_path_name(s, ".spack"))

    # spacks web utilities do not include direct copying of s3 objects, so we
    # need to download the archive locally, and then push it back to the target
    # location
    archive_stage_path = os.path.join(tmpdir, f"archive_stage_{s.name}_{s.dag_hash()}")
    archive_stage = spack.stage.Stage(v2_archive_url, path=archive_stage_path)

    try:
        archive_stage.create()
        archive_stage.fetch()
    except spack.error.FetchError:
        return MigrateSpecResult(False, f"Unable to fetch archive for {print_spec}")

    local_tarfile_path = archive_stage.save_filename

    # As long as we have to download the tarball anyway, we might as well compute the
    # checksum locally and check it against the expected value
    local_checksum = spack.util.crypto.checksum(
        spack.util.crypto.hash_fun_for_algo(algorithm), local_tarfile_path
    )

    if local_checksum != checksum:
        return MigrateSpecResult(
            False, f"Checksum mismatch for {print_spec}: expected {checksum}, got {local_checksum}"
        )

    spec_dict["archive_size"] = os.stat(local_tarfile_path).st_size

    # Compress the spec dict and compute its checksum
    metadata_checksum_algo = "sha256"
    spec_json_path = os.path.join(tmpdir, f"{s.name}_{s.dag_hash()}.spec.json")
    metadata_checksum, metadata_size = compressed_json_from_dict(
        spec_json_path, spec_dict, metadata_checksum_algo
    )

    tarball_blob_record = BlobRecord(
        spec_dict["archive_size"], v3_cache_class.TARBALL_MEDIATYPE, "gzip", algorithm, checksum
    )

    metadata_blob_record = BlobRecord(
        metadata_size,
        v3_cache_class.SPEC_MEDIATYPE,
        "gzip",
        metadata_checksum_algo,
        metadata_checksum,
    )

    # Compute the urls to the new blobs
    v3_archive_url = v3_cache_class.get_blob_url(mirror_url, tarball_blob_record)
    v3_spec_url = v3_cache_class.get_blob_url(mirror_url, metadata_blob_record)

    # First push the tarball
    tty.debug(f"Pushing {local_tarfile_path} to {v3_archive_url}")

    try:
        web_util.push_to_url(local_tarfile_path, v3_archive_url, keep_original=True)
    except Exception:
        return MigrateSpecResult(False, f"Failed to push archive for {print_spec}")

    # Then push the spec file
    tty.debug(f"Pushing {spec_json_path} to {v3_spec_url}")

    try:
        web_util.push_to_url(spec_json_path, v3_spec_url, keep_original=True)
    except Exception:
        return MigrateSpecResult(False, f"Failed to push spec metadata for {print_spec}")

    # Generate the manifest and write it to a temporary location
    manifest = {
        "version": v3_cache_class.get_layout_version(),
        "data": [tarball_blob_record.to_dict(), metadata_blob_record.to_dict()],
    }

    manifest_path = os.path.join(tmpdir, f"{s.dag_hash()}.manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=0, separators=(",", ":"))
        # Note: when using gpg clear sign, we need to avoid long lines (19995
        # chars). If lines are longer, they are truncated without error. So,
        # here we still add newlines, but no indent, so save on file size and
        # line length.

    # Possibly sign the manifest
    if not unsigned:
        manifest_path = sign_file(signing_key, manifest_path)

    v3_manifest_url = v3_cache_class.get_manifest_url(s, mirror_url)

    # Push the manifest
    try:
        web_util.push_to_url(manifest_path, v3_manifest_url, keep_original=True)
    except Exception:
        return MigrateSpecResult(False, f"Failed to push manifest for {print_spec}")

    return MigrateSpecResult(True, f"Successfully migrated {print_spec}")


def migrate(
    mirror: spack.mirrors.mirror.Mirror, unsigned: bool = False, delete_existing: bool = False
) -> None:
    """Perform migration of the given mirror

    If unsigned is True, signatures on signed specs will be ignored, and specs
    will not be re-signed before pushing to the new location.  Otherwise, spack
    will attempt to verify signatures and re-sign specs, and will fail if not
    able to do so.  If delete_existing is True, spack will delete the original
    contents of the mirror once the migration is complete."""
    signing_key = ""
    if not unsigned:
        try:
            signing_key = bindist.select_signing_key()
        except (bindist.NoKeyException, bindist.PickKeyException):
            raise MigrationException(
                "Signed migration requires exactly one secret key in keychain"
            )

    delete_action = "deleting" if delete_existing else "keeping"
    sign_action = "an unsigned" if unsigned else "a signed"
    mirror_url = mirror.fetch_url

    tty.msg(
        f"Performing {sign_action} migration of {mirror.push_url} "
        f"and {delete_action} existing contents"
    )

    index_url = url_util.join(mirror_url, "build_cache", spack_db.INDEX_JSON_FILE)
    contents = None

    try:
        _, _, index_file = web_util.read_from_url(index_url)
        contents = codecs.getreader("utf-8")(index_file).read()
    except (web_util.SpackWebError, OSError):
        raise MigrationException("Buildcache migration requires a buildcache index")

    with tempfile.TemporaryDirectory(dir=spack.stage.get_stage_root()) as tmpdir:
        index_path = os.path.join(tmpdir, "_tmp_index.json")
        with open(index_path, "w", encoding="utf-8") as fd:
            fd.write(contents)

        db = bindist.BuildCacheDatabase(tmpdir)
        db._read_from_file(pathlib.Path(index_path))

        specs_to_migrate = [
            s
            for s in db.query_local(installed=InstallRecordStatus.ANY)
            if not s.external and db.query_local_by_spec_hash(s.dag_hash()).in_buildcache
        ]

        # Run the tasks in parallel if possible
        executor = spack.util.parallel.make_concurrent_executor()
        migrate_futures = [
            executor.submit(_migrate_spec, spec, mirror_url, tmpdir, unsigned, signing_key)
            for spec in specs_to_migrate
        ]

        success_count = 0

        tty.msg("Migration summary:")
        for spec, migrate_future in zip(specs_to_migrate, migrate_futures):
            result = migrate_future.result()
            msg = f"  {spec.name}/{spec.dag_hash()[:7]}: {result.message}"
            if result.success:
                success_count += 1
                tty.msg(msg)
            else:
                tty.error(msg)
            # The migrated index should have the same specs as the original index,
            # modulo any specs that we failed to migrate for whatever reason. So
            # to avoid having to re-fetch all the spec files now, just mark them
            # appropriately in the existing database and push that.
            db.mark(spec, "in_buildcache", result.success)

        if success_count > 0:
            tty.msg("Updating index and pushing keys")

            # If the layout.json doesn't yet exist on this mirror, push it
            v3_cache_class = get_url_buildcache_class(layout_version=3)
            v3_cache_class.maybe_push_layout_json(mirror_url)

            # Push the migrated mirror index
            index_tmpdir = os.path.join(tmpdir, "rebuild_index")
            os.mkdir(index_tmpdir)
            bindist._push_index(db, index_tmpdir, mirror_url)

            # Push the public part of the signing key
            if not unsigned:
                keys_tmpdir = os.path.join(tmpdir, "keys")
                os.mkdir(keys_tmpdir)
                bindist._url_push_keys(
                    mirror_url, keys=[signing_key], update_index=True, tmpdir=keys_tmpdir
                )
        else:
            tty.warn("No specs migrated, did you mean to perform an unsigned migration instead?")

        # Delete the old layout if the user requested it
        if delete_existing:
            delete_prefix = url_util.join(mirror_url, "build_cache")
            tty.msg(f"Recursively deleting {delete_prefix}")
            web_util.remove_url(delete_prefix, recursive=True)

    tty.msg("Migration complete")
