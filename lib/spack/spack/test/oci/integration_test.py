# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# These are slow integration tests that do concretization, install, tarballing
# and compression. They still use an in-memory OCI registry.

import hashlib
import json
import os
from contextlib import contextmanager

import spack.oci.opener
from spack.binary_distribution import gzip_compressed_tarfile
from spack.main import SpackCommand
from spack.oci.image import Digest, ImageReference, default_config, default_manifest
from spack.oci.oci import blob_exists, get_manifest_and_config, upload_blob, upload_manifest
from spack.test.oci.mock_registry import DummyServer, InMemoryOCIRegistry, create_opener

buildcache = SpackCommand("buildcache")
mirror = SpackCommand("mirror")


@contextmanager
def oci_servers(*servers: DummyServer):
    old_opener = spack.oci.opener.urlopen
    spack.oci.opener.urlopen = create_opener(*servers).open
    yield
    spack.oci.opener.urlopen = old_opener


def test_buildcache_push_command(mutable_database, disable_parallel_buildcache_push):
    with oci_servers(InMemoryOCIRegistry("example.com")):
        mirror("add", "oci-test", "oci://example.com/image")

        # Push the package(s) to the OCI registry
        buildcache("push", "--update-index", "oci-test", "mpileaks^mpich")

        # Remove mpileaks from the database
        matches = mutable_database.query_local("mpileaks^mpich")
        assert len(matches) == 1
        spec = matches[0]
        spec.package.do_uninstall()

        # Reinstall mpileaks from the OCI registry
        buildcache("install", "--unsigned", "mpileaks^mpich")

        # Now it should be installed again
        assert spec.installed

        # And let's check that the bin/mpileaks executable is there
        assert os.path.exists(os.path.join(spec.prefix, "bin", "mpileaks"))


def test_buildcache_push_with_base_image_command(
    mutable_database, tmpdir, disable_parallel_buildcache_push
):
    """Test that we can push a package with a base image to an OCI registry.

    This test is a bit involved, cause we have to create a small base image."""

    registry_src = InMemoryOCIRegistry("src.example.com")
    registry_dst = InMemoryOCIRegistry("dst.example.com")

    base_image = ImageReference.from_string("src.example.com/my-base-image:latest")

    with oci_servers(registry_src, registry_dst):
        mirror("add", "oci-test", "oci://dst.example.com/image")

        # TODO: simplify creation of images...
        # We create a rootfs.tar.gz, a config file and a manifest file,
        # and upload those.

        config, manifest = default_config(architecture="amd64", os="linux"), default_manifest()

        # Create a small rootfs
        rootfs = tmpdir.join("rootfs")
        rootfs.ensure(dir=True)
        rootfs.join("bin").ensure(dir=True)
        rootfs.join("bin", "sh").ensure(file=True)

        # Create a tarball of it.
        tarball = tmpdir.join("base.tar.gz")
        with gzip_compressed_tarfile(tarball) as (tar, tar_gz_checksum, tar_checksum):
            tar.add(rootfs, arcname=".")

        tar_gz_digest = Digest.from_sha256(tar_gz_checksum.hexdigest())
        tar_digest = Digest.from_sha256(tar_checksum.hexdigest())

        # Save the config file
        config["rootfs"]["diff_ids"] = [str(tar_digest)]
        config_file = tmpdir.join("config.json")
        with open(config_file, "w") as f:
            f.write(json.dumps(config))

        config_digest = Digest.from_sha256(
            hashlib.sha256(open(config_file, "rb").read()).hexdigest()
        )

        # Register the layer in the manifest
        manifest["layers"].append(
            {
                "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
                "digest": str(tar_gz_digest),
                "size": tarball.size(),
            }
        )
        manifest["config"]["digest"] = str(config_digest)
        manifest["config"]["size"] = config_file.size()

        # Upload the layer and config file
        upload_blob(base_image, tarball, tar_gz_digest)
        upload_blob(base_image, config_file, config_digest)

        # Upload the manifest
        upload_manifest(base_image, manifest)

        # END TODO

        # Finally... use it as a base image
        buildcache("push", "--base-image", str(base_image), "oci-test", "mpileaks^mpich")

        # Figure out what tag was produced
        tag = next(tag for _, tag in registry_dst.manifests.keys() if tag.startswith("mpileaks-"))
        assert tag is not None

        # Fetch the manifest and config
        dst_image = ImageReference.from_string(f"dst.example.com/image:{tag}")
        retrieved_manifest, retrieved_config = get_manifest_and_config(dst_image)

        # Check that the base image layer is first.
        assert retrieved_manifest["layers"][0]["digest"] == str(tar_gz_digest)
        assert retrieved_config["rootfs"]["diff_ids"][0] == str(tar_digest)

        # And also check that we have layers for each link-run dependency
        matches = mutable_database.query_local("mpileaks^mpich")
        assert len(matches) == 1
        spec = matches[0]

        num_runtime_deps = len(list(spec.traverse(root=True, deptype=("link", "run"))))

        # One base layer + num_runtime_deps
        assert len(retrieved_manifest["layers"]) == 1 + num_runtime_deps

        # And verify that all layers including the base layer are present
        for layer in retrieved_manifest["layers"]:
            assert blob_exists(dst_image, digest=Digest.from_string(layer["digest"]))
