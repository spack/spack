# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import copy
import glob
import hashlib
import json
import multiprocessing
import multiprocessing.pool
import os
import shutil
import sys
import tempfile
import urllib.request
from typing import Dict, List, Optional, Tuple, Union

import llnl.util.tty as tty
from llnl.string import plural
from llnl.util.lang import elide_list

import spack.binary_distribution as bindist
import spack.cmd
import spack.config
import spack.environment as ev
import spack.error
import spack.hash_types as ht
import spack.mirror
import spack.oci.oci
import spack.oci.opener
import spack.relocate
import spack.repo
import spack.spec
import spack.stage
import spack.store
import spack.user_environment
import spack.util.crypto
import spack.util.url as url_util
import spack.util.web as web_util
from spack import traverse
from spack.build_environment import determine_number_of_jobs
from spack.cmd import display_specs
from spack.cmd.common import arguments
from spack.oci.image import (
    Digest,
    ImageReference,
    default_config,
    default_index_tag,
    default_manifest,
    default_tag,
    tag_is_spec,
)
from spack.oci.oci import (
    copy_missing_layers_with_retry,
    get_manifest_and_config_with_retry,
    upload_blob_with_retry,
    upload_manifest_with_retry,
)
from spack.spec import Spec, save_dependency_specfiles

description = "create, download and install binary packages"
section = "packaging"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser):
    setattr(setup_parser, "parser", subparser)
    subparsers = subparser.add_subparsers(help="buildcache sub-commands")

    push = subparsers.add_parser("push", aliases=["create"], help=push_fn.__doc__)
    push.add_argument("-f", "--force", action="store_true", help="overwrite tarball if it exists")
    push.add_argument(
        "--allow-root",
        "-a",
        action="store_true",
        help="allow install root string in binary files after RPATH substitution",
    )
    push_sign = push.add_mutually_exclusive_group(required=False)
    push_sign.add_argument(
        "--unsigned",
        "-u",
        action="store_false",
        dest="signed",
        default=None,
        help="push unsigned buildcache tarballs",
    )
    push_sign.add_argument(
        "--signed",
        action="store_true",
        dest="signed",
        default=None,
        help="push signed buildcache tarballs",
    )
    push_sign.add_argument(
        "--key", "-k", metavar="key", type=str, default=None, help="key for signing"
    )
    push.add_argument(
        "mirror", type=arguments.mirror_name_or_url, help="mirror name, path, or URL"
    )
    push.add_argument(
        "--update-index",
        "--rebuild-index",
        action="store_true",
        default=False,
        help="regenerate buildcache index after building package(s)",
    )
    push.add_argument(
        "--spec-file", default=None, help="create buildcache entry for spec from json or yaml file"
    )
    push.add_argument(
        "--only",
        default="package,dependencies",
        dest="things_to_install",
        choices=["package", "dependencies"],
        help="select the buildcache mode. "
        "The default is to build a cache for the package along with all its dependencies. "
        "Alternatively, one can decide to build a cache for only the package or only the "
        "dependencies",
    )
    push.add_argument(
        "--fail-fast",
        action="store_true",
        help="stop pushing on first failure (default is best effort)",
    )
    push.add_argument(
        "--base-image", default=None, help="specify the base image for the buildcache"
    )
    push.add_argument(
        "--tag",
        "-t",
        default=None,
        help="when pushing to an OCI registry, tag an image containing all root specs and their "
        "runtime dependencies",
    )
    arguments.add_common_arguments(push, ["specs", "jobs"])
    push.set_defaults(func=push_fn)

    install = subparsers.add_parser("install", help=install_fn.__doc__)
    install.add_argument(
        "-f", "--force", action="store_true", help="overwrite install directory if it exists"
    )
    install.add_argument(
        "-m", "--multiple", action="store_true", help="allow all matching packages"
    )
    install.add_argument(
        "-u",
        "--unsigned",
        action="store_true",
        help="install unsigned buildcache tarballs for testing",
    )
    install.add_argument(
        "-o",
        "--otherarch",
        action="store_true",
        help="install specs from other architectures instead of default platform and OS",
    )

    arguments.add_common_arguments(install, ["specs"])
    install.set_defaults(func=install_fn)

    listcache = subparsers.add_parser("list", help=list_fn.__doc__)
    arguments.add_common_arguments(listcache, ["long", "very_long", "namespaces"])
    listcache.add_argument(
        "-v",
        "--variants",
        action="store_true",
        dest="variants",
        help="show variants in output (can be long)",
    )
    listcache.add_argument(
        "-a",
        "--allarch",
        action="store_true",
        help="list specs for all available architectures instead of default platform and OS",
    )
    arguments.add_common_arguments(listcache, ["specs"])
    listcache.set_defaults(func=list_fn)

    keys = subparsers.add_parser("keys", help=keys_fn.__doc__)
    keys.add_argument(
        "-i", "--install", action="store_true", help="install Keys pulled from mirror"
    )
    keys.add_argument("-t", "--trust", action="store_true", help="trust all downloaded keys")
    keys.add_argument("-f", "--force", action="store_true", help="force new download of keys")
    keys.set_defaults(func=keys_fn)

    preview = subparsers.add_parser("preview", help=preview_fn.__doc__)
    arguments.add_common_arguments(preview, ["installed_specs"])
    preview.set_defaults(func=preview_fn)

    # Check if binaries need to be rebuilt on remote mirror
    check = subparsers.add_parser("check", help=check_fn.__doc__)
    check.add_argument(
        "-m",
        "--mirror-url",
        default=None,
        help="override any configured mirrors with this mirror URL",
    )

    check.add_argument(
        "-o", "--output-file", default=None, help="file where rebuild info should be written"
    )

    # used to construct scope arguments below
    check.add_argument(
        "--scope",
        action=arguments.ConfigScope,
        default=lambda: spack.config.default_modify_scope(),
        help="configuration scope containing mirrors to check",
    )
    # Unfortunately there are 3 ways to do the same thing here:
    check_specs = check.add_mutually_exclusive_group()
    check_specs.add_argument(
        "-s", "--spec", help="check single spec instead of release specs file"
    )
    check_specs.add_argument(
        "--spec-file",
        help="check single spec from json or yaml file instead of release specs file",
    )
    arguments.add_common_arguments(check, ["specs"])

    check.set_defaults(func=check_fn)

    # Download tarball and specfile
    download = subparsers.add_parser("download", help=download_fn.__doc__)
    download_spec_or_specfile = download.add_mutually_exclusive_group(required=True)
    download_spec_or_specfile.add_argument(
        "-s", "--spec", help="download built tarball for spec from mirror"
    )
    download_spec_or_specfile.add_argument(
        "--spec-file", help="download built tarball for spec (from json or yaml file) from mirror"
    )
    download.add_argument(
        "-p",
        "--path",
        required=True,
        default=None,
        help="path to directory where tarball should be downloaded",
    )
    download.set_defaults(func=download_fn)

    # Get buildcache name
    getbuildcachename = subparsers.add_parser(
        "get-buildcache-name", help=get_buildcache_name_fn.__doc__
    )
    getbuildcachename_spec_or_specfile = getbuildcachename.add_mutually_exclusive_group(
        required=True
    )
    getbuildcachename_spec_or_specfile.add_argument(
        "-s", "--spec", help="spec string for which buildcache name is desired"
    )
    getbuildcachename_spec_or_specfile.add_argument(
        "--spec-file", help="path to spec json or yaml file for which buildcache name is desired"
    )
    getbuildcachename.set_defaults(func=get_buildcache_name_fn)

    # Given the root spec, save the yaml of the dependent spec to a file
    savespecfile = subparsers.add_parser("save-specfile", help=save_specfile_fn.__doc__)
    savespecfile_spec_or_specfile = savespecfile.add_mutually_exclusive_group(required=True)
    savespecfile_spec_or_specfile.add_argument("--root-spec", help="root spec of dependent spec")
    savespecfile_spec_or_specfile.add_argument(
        "--root-specfile", help="path to json or yaml file containing root spec of dependent spec"
    )
    savespecfile.add_argument(
        "-s",
        "--specs",
        required=True,
        help="list of dependent specs for which saved yaml is desired",
    )
    savespecfile.add_argument(
        "--specfile-dir", required=True, help="path to directory where spec yamls should be saved"
    )
    savespecfile.set_defaults(func=save_specfile_fn)

    # Sync buildcache entries from one mirror to another
    sync = subparsers.add_parser("sync", help=sync_fn.__doc__)
    sync.add_argument(
        "--manifest-glob", help="a quoted glob pattern identifying copy manifest files"
    )
    sync.add_argument(
        "src_mirror",
        metavar="source mirror",
        type=arguments.mirror_name_or_url,
        nargs="?",
        help="source mirror name, path, or URL",
    )
    sync.add_argument(
        "dest_mirror",
        metavar="destination mirror",
        type=arguments.mirror_name_or_url,
        nargs="?",
        help="destination mirror name, path, or URL",
    )
    sync.set_defaults(func=sync_fn)

    # Update buildcache index without copying any additional packages
    update_index = subparsers.add_parser(
        "update-index", aliases=["rebuild-index"], help=update_index_fn.__doc__
    )
    update_index.add_argument(
        "mirror", type=arguments.mirror_name_or_url, help="destination mirror name, path, or URL"
    )
    update_index.add_argument(
        "-k",
        "--keys",
        default=False,
        action="store_true",
        help="if provided, key index will be updated as well as package index",
    )
    update_index.set_defaults(func=update_index_fn)


def _matching_specs(specs: List[Spec]) -> List[Spec]:
    """Disambiguate specs and return a list of matching specs"""
    return [spack.cmd.disambiguate_spec(s, ev.active_environment(), installed=any) for s in specs]


def _format_spec(spec: Spec) -> str:
    return spec.cformat("{name}{@version}{/hash:7}")


def _progress(i: int, total: int):
    if total > 1:
        digits = len(str(total))
        return f"[{i+1:{digits}}/{total}] "
    return ""


class NoPool:
    def map(self, func, args):
        return [func(a) for a in args]

    def starmap(self, func, args):
        return [func(*a) for a in args]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


MaybePool = Union[multiprocessing.pool.Pool, NoPool]


def _make_pool() -> MaybePool:
    """Can't use threading because it's unsafe, and can't use spawned processes because of globals.
    That leaves only forking"""
    if multiprocessing.get_start_method() == "fork":
        return multiprocessing.pool.Pool(determine_number_of_jobs(parallel=True))
    else:
        return NoPool()


def push_fn(args):
    """create a binary package and push it to a mirror"""
    if args.spec_file:
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            "Use positional arguments instead."
        )

    if args.specs or args.spec_file:
        roots = _matching_specs(spack.cmd.parse_specs(args.specs or args.spec_file))
    else:
        roots = spack.cmd.require_active_env(cmd_name="buildcache push").concrete_roots()

    if args.allow_root:
        tty.warn(
            "The flag `--allow-root` is the default in Spack 0.21, will be removed in Spack 0.22"
        )

    mirror: spack.mirror.Mirror = args.mirror

    # Check if this is an OCI image.
    try:
        target_image = spack.oci.oci.image_from_mirror(mirror)
    except ValueError:
        target_image = None

    push_url = mirror.push_url

    # When neither --signed, --unsigned nor --key are specified, use the mirror's default.
    if args.signed is None and not args.key:
        unsigned = not mirror.signed
    else:
        unsigned = not (args.key or args.signed)

    # For OCI images, we require dependencies to be pushed for now.
    if target_image:
        if "dependencies" not in args.things_to_install:
            tty.die("Dependencies must be pushed for OCI images.")
        if not unsigned:
            tty.warn(
                "Code signing is currently not supported for OCI images. "
                "Use --unsigned to silence this warning."
            )

    # This is a list of installed, non-external specs.
    specs = bindist.specs_to_be_packaged(
        roots,
        root="package" in args.things_to_install,
        dependencies="dependencies" in args.things_to_install,
    )

    # When pushing multiple specs, print the url once ahead of time, as well as how
    # many specs are being pushed.
    if len(specs) > 1:
        tty.info(f"Selected {len(specs)} specs to push to {push_url}")

    failed = []

    # TODO: unify this logic in the future.
    if target_image:
        base_image = ImageReference.from_string(args.base_image) if args.base_image else None
        with tempfile.TemporaryDirectory(
            dir=spack.stage.get_stage_root()
        ) as tmpdir, _make_pool() as pool:
            skipped, base_images, checksums = _push_oci(
                target_image=target_image,
                base_image=base_image,
                installed_specs_with_deps=specs,
                force=args.force,
                tmpdir=tmpdir,
                pool=pool,
            )

            # Apart from creating manifests for each individual spec, we allow users to create a
            # separate image tag for all root specs and their runtime dependencies.
            if args.tag:
                tagged_image = target_image.with_tag(args.tag)
                # _push_oci may not populate base_images if binaries were already in the registry
                for spec in roots:
                    _update_base_images(
                        base_image=base_image,
                        target_image=target_image,
                        spec=spec,
                        base_image_cache=base_images,
                    )
                _put_manifest(base_images, checksums, tagged_image, tmpdir, None, None, *roots)
                tty.info(f"Tagged {tagged_image}")

    else:
        skipped = []

        for i, spec in enumerate(specs):
            try:
                bindist.push_or_raise(
                    spec,
                    push_url,
                    bindist.PushOptions(
                        force=args.force,
                        unsigned=unsigned,
                        key=args.key,
                        regenerate_index=args.update_index,
                    ),
                )

                msg = f"{_progress(i, len(specs))}Pushed {_format_spec(spec)}"
                if len(specs) == 1:
                    msg += f" to {push_url}"
                tty.info(msg)

            except bindist.NoOverwriteException:
                skipped.append(_format_spec(spec))

            # Catch any other exception unless the fail fast option is set
            except Exception as e:
                if args.fail_fast or isinstance(
                    e, (bindist.PickKeyException, bindist.NoKeyException)
                ):
                    raise
                failed.append((_format_spec(spec), e))

    if skipped:
        if len(specs) == 1:
            tty.info("The spec is already in the buildcache. Use --force to overwrite it.")
        elif len(skipped) == len(specs):
            tty.info("All specs are already in the buildcache. Use --force to overwrite them.")
        else:
            tty.info(
                "The following {} specs were skipped as they already exist in the buildcache:\n"
                "    {}\n"
                "    Use --force to overwrite them.".format(
                    len(skipped), ", ".join(elide_list(skipped, 5))
                )
            )

    if failed:
        if len(failed) == 1:
            raise failed[0][1]

        raise spack.error.SpackError(
            f"The following {len(failed)} errors occurred while pushing specs to the buildcache",
            "\n".join(
                elide_list([f"    {spec}: {e.__class__.__name__}: {e}" for spec, e in failed], 5)
            ),
        )

    # Update the index if requested
    # TODO: remove update index logic out of bindist; should be once after all specs are pushed
    # not once per spec.
    if target_image and len(skipped) < len(specs) and args.update_index:
        with tempfile.TemporaryDirectory(
            dir=spack.stage.get_stage_root()
        ) as tmpdir, _make_pool() as pool:
            _update_index_oci(target_image, tmpdir, pool)


def _get_spack_binary_blob(image_ref: ImageReference) -> Optional[spack.oci.oci.Blob]:
    """Get the spack tarball layer digests and size if it exists"""
    try:
        manifest, config = get_manifest_and_config_with_retry(image_ref)

        return spack.oci.oci.Blob(
            compressed_digest=Digest.from_string(manifest["layers"][-1]["digest"]),
            uncompressed_digest=Digest.from_string(config["rootfs"]["diff_ids"][-1]),
            size=manifest["layers"][-1]["size"],
        )
    except Exception:
        return None


def _push_single_spack_binary_blob(image_ref: ImageReference, spec: spack.spec.Spec, tmpdir: str):
    filename = os.path.join(tmpdir, f"{spec.dag_hash()}.tar.gz")

    # Create an oci.image.layer aka tarball of the package
    compressed_tarfile_checksum, tarfile_checksum = spack.oci.oci.create_tarball(spec, filename)

    blob = spack.oci.oci.Blob(
        Digest.from_sha256(compressed_tarfile_checksum),
        Digest.from_sha256(tarfile_checksum),
        os.path.getsize(filename),
    )

    # Upload the blob
    upload_blob_with_retry(image_ref, file=filename, digest=blob.compressed_digest)

    # delete the file
    os.unlink(filename)

    return blob


def _retrieve_env_dict_from_config(config: dict) -> dict:
    """Retrieve the environment variables from the image config file.
    Sets a default value for PATH if it is not present.

    Args:
        config (dict): The image config file.

    Returns:
        dict: The environment variables.
    """
    env = {"PATH": "/bin:/usr/bin"}

    if "Env" in config.get("config", {}):
        for entry in config["config"]["Env"]:
            key, value = entry.split("=", 1)
            env[key] = value
    return env


def _archspec_to_gooarch(spec: spack.spec.Spec) -> str:
    name = spec.target.family.name
    name_map = {"aarch64": "arm64", "x86_64": "amd64"}
    return name_map.get(name, name)


def _put_manifest(
    base_images: Dict[str, Tuple[dict, dict]],
    checksums: Dict[str, spack.oci.oci.Blob],
    image_ref: ImageReference,
    tmpdir: str,
    extra_config: Optional[dict],
    annotations: Optional[dict],
    *specs: spack.spec.Spec,
):
    architecture = _archspec_to_gooarch(specs[0])

    dependencies = list(
        reversed(
            list(
                s
                for s in traverse.traverse_nodes(
                    specs, order="topo", deptype=("link", "run"), root=True
                )
                if not s.external
            )
        )
    )

    base_manifest, base_config = base_images[architecture]
    env = _retrieve_env_dict_from_config(base_config)

    # If the base image uses `vnd.docker.distribution.manifest.v2+json`, then we use that too.
    # This is because Singularity / Apptainer is very strict about not mixing them.
    base_manifest_mediaType = base_manifest.get(
        "mediaType", "application/vnd.oci.image.manifest.v1+json"
    )
    use_docker_format = (
        base_manifest_mediaType == "application/vnd.docker.distribution.manifest.v2+json"
    )

    spack.user_environment.environment_modifications_for_specs(*specs).apply_modifications(env)

    # Create an oci.image.config file
    config = copy.deepcopy(base_config)

    # Add the diff ids of the dependencies
    for s in dependencies:
        config["rootfs"]["diff_ids"].append(str(checksums[s.dag_hash()].uncompressed_digest))

    # Set the environment variables
    config["config"]["Env"] = [f"{k}={v}" for k, v in env.items()]

    if extra_config:
        # From the OCI v1.0 spec:
        # > Any extra fields in the Image JSON struct are considered implementation
        # > specific and MUST be ignored by any implementations which are unable to
        # > interpret them.
        config.update(extra_config)

    config_file = os.path.join(tmpdir, f"{specs[0].dag_hash()}.config.json")

    with open(config_file, "w") as f:
        json.dump(config, f, separators=(",", ":"))

    config_file_checksum = Digest.from_sha256(
        spack.util.crypto.checksum(hashlib.sha256, config_file)
    )

    # Upload the config file
    upload_blob_with_retry(image_ref, file=config_file, digest=config_file_checksum)

    manifest = {
        "mediaType": base_manifest_mediaType,
        "schemaVersion": 2,
        "config": {
            "mediaType": base_manifest["config"]["mediaType"],
            "digest": str(config_file_checksum),
            "size": os.path.getsize(config_file),
        },
        "layers": [
            *(layer for layer in base_manifest["layers"]),
            *(
                {
                    "mediaType": (
                        "application/vnd.docker.image.rootfs.diff.tar.gzip"
                        if use_docker_format
                        else "application/vnd.oci.image.layer.v1.tar+gzip"
                    ),
                    "digest": str(checksums[s.dag_hash()].compressed_digest),
                    "size": checksums[s.dag_hash()].size,
                }
                for s in dependencies
            ),
        ],
    }

    if not use_docker_format and annotations:
        manifest["annotations"] = annotations

    # Finally upload the manifest
    upload_manifest_with_retry(image_ref, manifest=manifest)

    # delete the config file
    os.unlink(config_file)


def _update_base_images(
    *,
    base_image: Optional[ImageReference],
    target_image: ImageReference,
    spec: spack.spec.Spec,
    base_image_cache: Dict[str, Tuple[dict, dict]],
):
    """For a given spec and base image, copy the missing layers of the base image with matching
    arch to the registry of the target image. If no base image is specified, create a dummy
    manifest and config file."""
    architecture = _archspec_to_gooarch(spec)
    if architecture in base_image_cache:
        return
    if base_image is None:
        base_image_cache[architecture] = (
            default_manifest(),
            default_config(architecture, "linux"),
        )
    else:
        base_image_cache[architecture] = copy_missing_layers_with_retry(
            base_image, target_image, architecture
        )


def _push_oci(
    *,
    target_image: ImageReference,
    base_image: Optional[ImageReference],
    installed_specs_with_deps: List[Spec],
    tmpdir: str,
    pool: MaybePool,
    force: bool = False,
) -> Tuple[List[str], Dict[str, Tuple[dict, dict]], Dict[str, spack.oci.oci.Blob]]:
    """Push specs to an OCI registry

    Args:
        image_ref: The target OCI image
        base_image: Optional base image, which will be copied to the target registry.
        installed_specs_with_deps: The installed specs to push, excluding externals,
            including deps, ordered from roots to leaves.
        force: Whether to overwrite existing layers and manifests in the buildcache.

    Returns:
        A tuple consisting of the list of skipped specs already in the build cache,
        a dictionary mapping architectures to base image manifests and configs,
        and a dictionary mapping each spec's dag hash to a blob.
    """

    # Reverse the order
    installed_specs_with_deps = list(reversed(installed_specs_with_deps))

    # Spec dag hash -> blob
    checksums: Dict[str, spack.oci.oci.Blob] = {}

    # arch -> (manifest, config)
    base_images: Dict[str, Tuple[dict, dict]] = {}

    # Specs not uploaded because they already exist
    skipped = []

    if not force:
        tty.info("Checking for existing specs in the buildcache")
        to_be_uploaded = []

        tags_to_check = (target_image.with_tag(default_tag(s)) for s in installed_specs_with_deps)
        available_blobs = pool.map(_get_spack_binary_blob, tags_to_check)

        for spec, maybe_blob in zip(installed_specs_with_deps, available_blobs):
            if maybe_blob is not None:
                checksums[spec.dag_hash()] = maybe_blob
                skipped.append(_format_spec(spec))
            else:
                to_be_uploaded.append(spec)
    else:
        to_be_uploaded = installed_specs_with_deps

    if not to_be_uploaded:
        return skipped, base_images, checksums

    tty.info(
        f"{len(to_be_uploaded)} specs need to be pushed to "
        f"{target_image.domain}/{target_image.name}"
    )

    # Upload blobs
    new_blobs = pool.starmap(
        _push_single_spack_binary_blob, ((target_image, spec, tmpdir) for spec in to_be_uploaded)
    )

    # And update the spec to blob mapping
    for spec, blob in zip(to_be_uploaded, new_blobs):
        checksums[spec.dag_hash()] = blob

    # Copy base images if necessary
    for spec in to_be_uploaded:
        _update_base_images(
            base_image=base_image,
            target_image=target_image,
            spec=spec,
            base_image_cache=base_images,
        )

    def extra_config(spec: Spec):
        spec_dict = spec.to_dict(hash=ht.dag_hash)
        spec_dict["buildcache_layout_version"] = 1
        spec_dict["binary_cache_checksum"] = {
            "hash_algorithm": "sha256",
            "hash": checksums[spec.dag_hash()].compressed_digest.digest,
        }
        return spec_dict

    # Upload manifests
    tty.info("Uploading manifests")
    pool.starmap(
        _put_manifest,
        (
            (
                base_images,
                checksums,
                target_image.with_tag(default_tag(spec)),
                tmpdir,
                extra_config(spec),
                {"org.opencontainers.image.description": spec.format()},
                spec,
            )
            for spec in to_be_uploaded
        ),
    )

    # Print the image names of the top-level specs
    for spec in to_be_uploaded:
        tty.info(f"Pushed {_format_spec(spec)} to {target_image.with_tag(default_tag(spec))}")

    return skipped, base_images, checksums


def _config_from_tag(image_ref: ImageReference, tag: str) -> Optional[dict]:
    # Don't allow recursion here, since Spack itself always uploads
    # vnd.oci.image.manifest.v1+json, not vnd.oci.image.index.v1+json
    _, config = get_manifest_and_config_with_retry(image_ref.with_tag(tag), tag, recurse=0)

    # Do very basic validation: if "spec" is a key in the config, it
    # must be a Spec object too.
    return config if "spec" in config else None


def _update_index_oci(image_ref: ImageReference, tmpdir: str, pool: MaybePool) -> None:
    request = urllib.request.Request(url=image_ref.tags_url())
    response = spack.oci.opener.urlopen(request)
    spack.oci.opener.ensure_status(request, response, 200)
    tags = json.load(response)["tags"]

    # Fetch all image config files in parallel
    spec_dicts = pool.starmap(
        _config_from_tag, ((image_ref, tag) for tag in tags if tag_is_spec(tag))
    )

    # Populate the database
    db_root_dir = os.path.join(tmpdir, "db_root")
    db = bindist.BuildCacheDatabase(db_root_dir)

    for spec_dict in spec_dicts:
        spec = Spec.from_dict(spec_dict)
        db.add(spec, directory_layout=None)
        db.mark(spec, "in_buildcache", True)

    # Create the index.json file
    index_json_path = os.path.join(tmpdir, "index.json")
    with open(index_json_path, "w") as f:
        db._write_to_file(f)

    # Create an empty config.json file
    empty_config_json_path = os.path.join(tmpdir, "config.json")
    with open(empty_config_json_path, "wb") as f:
        f.write(b"{}")

    # Upload the index.json file
    index_shasum = Digest.from_sha256(spack.util.crypto.checksum(hashlib.sha256, index_json_path))
    upload_blob_with_retry(image_ref, file=index_json_path, digest=index_shasum)

    # Upload the config.json file
    empty_config_digest = Digest.from_sha256(
        spack.util.crypto.checksum(hashlib.sha256, empty_config_json_path)
    )
    upload_blob_with_retry(image_ref, file=empty_config_json_path, digest=empty_config_digest)

    # Push a manifest file that references the index.json file as a layer
    # Notice that we push this as if it is an image, which it of course is not.
    # When the ORAS spec becomes official, we can use that instead of a fake image.
    # For now we just use the OCI image spec, so that we don't run into issues with
    # automatic garbage collection of blobs that are not referenced by any image manifest.
    oci_manifest = {
        "mediaType": "application/vnd.oci.image.manifest.v1+json",
        "schemaVersion": 2,
        # Config is just an empty {} file for now, and irrelevant
        "config": {
            "mediaType": "application/vnd.oci.image.config.v1+json",
            "digest": str(empty_config_digest),
            "size": os.path.getsize(empty_config_json_path),
        },
        # The buildcache index is the only layer, and is not a tarball, we lie here.
        "layers": [
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                "digest": str(index_shasum),
                "size": os.path.getsize(index_json_path),
            }
        ],
    }

    upload_manifest_with_retry(image_ref.with_tag(default_index_tag), oci_manifest)


def install_fn(args):
    """install from a binary package"""
    if not args.specs:
        tty.die("a spec argument is required to install from a buildcache")

    query = bindist.BinaryCacheQuery(all_architectures=args.otherarch)
    matches = spack.store.find(args.specs, multiple=args.multiple, query_fn=query)
    for match in matches:
        bindist.install_single_spec(match, unsigned=args.unsigned, force=args.force)


def list_fn(args):
    """list binary packages available from mirrors"""
    try:
        specs = bindist.update_cache_and_get_specs()
    except bindist.FetchCacheError as e:
        tty.die(e)

    if not args.allarch:
        arch = spack.spec.Spec.default_arch()
        specs = [s for s in specs if s.intersects(arch)]

    if args.specs:
        constraints = set(args.specs)
        specs = [s for s in specs if any(s.intersects(c) for c in constraints)]
    if sys.stdout.isatty():
        builds = len(specs)
        tty.msg("%s." % plural(builds, "cached build"))
        if not builds and not args.allarch:
            tty.msg(
                "You can query all available architectures with:",
                "spack buildcache list --allarch",
            )
    display_specs(specs, args, all_headers=True)


def keys_fn(args):
    """get public keys available on mirrors"""
    bindist.get_keys(args.install, args.trust, args.force)


def preview_fn(args):
    """analyze an installed spec and reports whether executables and libraries are relocatable"""
    tty.warn(
        "`spack buildcache preview` is deprecated since `spack buildcache push --allow-root` is "
        "now the default. This command will be removed in Spack 0.22"
    )


def check_fn(args: argparse.Namespace):
    """check specs against remote binary mirror(s) to see if any need to be rebuilt

    this command uses the process exit code to indicate its result, specifically, if the
    exit code is non-zero, then at least one of the indicated specs needs to be rebuilt
    """
    if args.spec_file:
        specs_arg = (
            args.spec_file if os.path.sep in args.spec_file else os.path.join(".", args.spec_file)
        )
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            f"Use `spack buildcache check {specs_arg}` instead."
        )
    elif args.spec:
        specs_arg = args.spec
        tty.warn(
            "The flag `--spec` is deprecated and will be removed in Spack 0.23. "
            f"Use `spack buildcache check {specs_arg}` instead."
        )
    else:
        specs_arg = args.specs

    if specs_arg:
        specs = _matching_specs(spack.cmd.parse_specs(specs_arg))
    else:
        specs = spack.cmd.require_active_env("buildcache check").all_specs()

    if not specs:
        tty.msg("No specs provided, exiting.")
        return

    for spec in specs:
        spec.concretize()

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get("mirrors", scope=args.scope)

    if args.mirror_url:
        configured_mirrors = {"additionalMirrorUrl": args.mirror_url}

    if not configured_mirrors:
        tty.msg("No mirrors provided, exiting.")
        return

    if bindist.check_specs_against_mirrors(configured_mirrors, specs, args.output_file) == 1:
        sys.exit(1)


def download_fn(args):
    """download buildcache entry from a remote mirror to local folder

    this command uses the process exit code to indicate its result, specifically, a non-zero exit
    code indicates that the command failed to download at least one of the required buildcache
    components
    """
    if args.spec_file:
        tty.warn(
            "The flag `--spec-file` is deprecated and will be removed in Spack 0.22. "
            "Use --spec instead."
        )

    specs = _matching_specs(spack.cmd.parse_specs(args.spec or args.spec_file))

    if len(specs) != 1:
        tty.die("a single spec argument is required to download from a buildcache")

    if not bindist.download_single_spec(specs[0], args.path):
        sys.exit(1)


def get_buildcache_name_fn(args):
    """get name (prefix) of buildcache entries for this spec"""
    tty.warn("This command is deprecated and will be removed in Spack 0.22.")
    specs = _matching_specs(spack.cmd.parse_specs(args.spec or args.spec_file))
    if len(specs) != 1:
        tty.die("a single spec argument is required to get buildcache name")
    print(bindist.tarball_name(specs[0], ""))


def save_specfile_fn(args):
    """get full spec for dependencies and write them to files in the specified output directory

    uses exit code to signal success or failure. an exit code of zero means the command was likely
    successful. if any errors or exceptions are encountered, or if expected command-line arguments
    are not provided, then the exit code will be non-zero
    """
    if args.root_specfile:
        tty.warn(
            "The flag `--root-specfile` is deprecated and will be removed in Spack 0.22. "
            "Use --root-spec instead."
        )

    specs = spack.cmd.parse_specs(args.root_spec or args.root_specfile)

    if len(specs) != 1:
        tty.die("a single spec argument is required to save specfile")

    root = specs[0]

    if not root.concrete:
        root.concretize()

    save_dependency_specfiles(
        root, args.specfile_dir, dependencies=spack.cmd.parse_specs(args.specs)
    )


def copy_buildcache_file(src_url, dest_url, local_path=None):
    """Copy from source url to destination url"""
    tmpdir = None

    if not local_path:
        tmpdir = tempfile.mkdtemp()
        local_path = os.path.join(tmpdir, os.path.basename(src_url))

    try:
        temp_stage = spack.stage.Stage(src_url, path=os.path.dirname(local_path))
        try:
            temp_stage.create()
            temp_stage.fetch()
            web_util.push_to_url(local_path, dest_url, keep_original=True)
        except spack.error.FetchError as e:
            # Expected, since we have to try all the possible extensions
            tty.debug("no such file: {0}".format(src_url))
            tty.debug(e)
        finally:
            temp_stage.destroy()
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


def sync_fn(args):
    """sync binaries (and associated metadata) from one mirror to another

    requires an active environment in order to know which specs to sync
    """
    if args.manifest_glob:
        manifest_copy(glob.glob(args.manifest_glob))
        return 0

    if args.src_mirror is None or args.dest_mirror is None:
        tty.die("Provide mirrors to sync from and to.")

    src_mirror = args.src_mirror
    dest_mirror = args.dest_mirror

    src_mirror_url = src_mirror.fetch_url
    dest_mirror_url = dest_mirror.push_url

    # Get the active environment
    env = spack.cmd.require_active_env(cmd_name="buildcache sync")

    tty.msg(
        "Syncing environment buildcache files from {0} to {1}".format(
            src_mirror_url, dest_mirror_url
        )
    )

    build_cache_dir = bindist.build_cache_relative_path()
    buildcache_rel_paths = []

    tty.debug("Syncing the following specs:")
    for s in env.all_specs():
        tty.debug("  {0}{1}: {2}".format("* " if s in env.roots() else "  ", s.name, s.dag_hash()))

        buildcache_rel_paths.extend(
            [
                os.path.join(build_cache_dir, bindist.tarball_path_name(s, ".spack")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.json.sig")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.json")),
                os.path.join(build_cache_dir, bindist.tarball_name(s, ".spec.yaml")),
            ]
        )

    tmpdir = tempfile.mkdtemp()

    try:
        for rel_path in buildcache_rel_paths:
            src_url = url_util.join(src_mirror_url, rel_path)
            local_path = os.path.join(tmpdir, rel_path)
            dest_url = url_util.join(dest_mirror_url, rel_path)

            tty.debug("Copying {0} to {1} via {2}".format(src_url, dest_url, local_path))
            copy_buildcache_file(src_url, dest_url, local_path=local_path)
    finally:
        shutil.rmtree(tmpdir)


def manifest_copy(manifest_file_list):
    """Read manifest files containing information about specific specs to copy
    from source to destination, remove duplicates since any binary packge for
    a given hash should be the same as any other, and copy all files specified
    in the manifest files."""
    deduped_manifest = {}

    for manifest_path in manifest_file_list:
        with open(manifest_path) as fd:
            manifest = json.loads(fd.read())
            for spec_hash, copy_list in manifest.items():
                # Last duplicate hash wins
                deduped_manifest[spec_hash] = copy_list

    for spec_hash, copy_list in deduped_manifest.items():
        for copy_file in copy_list:
            tty.debug("copying {0} to {1}".format(copy_file["src"], copy_file["dest"]))
            copy_buildcache_file(copy_file["src"], copy_file["dest"])


def update_index(mirror: spack.mirror.Mirror, update_keys=False):
    # Special case OCI images for now.
    try:
        image_ref = spack.oci.oci.image_from_mirror(mirror)
    except ValueError:
        image_ref = None

    if image_ref:
        with tempfile.TemporaryDirectory(
            dir=spack.stage.get_stage_root()
        ) as tmpdir, _make_pool() as pool:
            _update_index_oci(image_ref, tmpdir, pool)
        return

    # Otherwise, assume a normal mirror.
    url = mirror.push_url

    bindist.generate_package_index(url_util.join(url, bindist.build_cache_relative_path()))

    if update_keys:
        keys_url = url_util.join(
            url, bindist.build_cache_relative_path(), bindist.build_cache_keys_relative_path()
        )

        bindist.generate_key_index(keys_url)


def update_index_fn(args):
    """update a buildcache index"""
    update_index(args.mirror, update_keys=args.keys)


def buildcache(parser, args):
    if args.func:
        args.func(args)
