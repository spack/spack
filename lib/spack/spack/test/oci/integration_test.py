# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# These are slow integration tests that do concretization, install, tarballing
# and compression. They still use an in-memory OCI registry.

import hashlib
import json
import os
import pathlib
from contextlib import contextmanager

import spack.environment as ev
import spack.oci.opener
from spack.main import SpackCommand
from spack.oci.image import Digest, ImageReference, default_config, default_manifest
from spack.oci.oci import blob_exists, get_manifest_and_config, upload_blob, upload_manifest
from spack.test.oci.mock_registry import DummyServer, InMemoryOCIRegistry, create_opener
from spack.util.archive import gzip_compressed_tarfile

buildcache = SpackCommand("buildcache")
mirror = SpackCommand("mirror")
env = SpackCommand("env")
install = SpackCommand("install")


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


def test_buildcache_tag(
    install_mockery, mock_fetch, mutable_mock_env_path, disable_parallel_buildcache_push
):
    """Tests whether we can create an OCI image from a full environment with multiple roots."""
    env("create", "test")
    with ev.read("test"):
        install("--add", "libelf")
        install("--add", "trivial-install-test-package")

    registry = InMemoryOCIRegistry("example.com")

    with oci_servers(registry):
        mirror("add", "oci-test", "oci://example.com/image")

        with ev.read("test"):
            buildcache("push", "--tag", "full_env", "oci-test")

        name = ImageReference.from_string("example.com/image:full_env")

        with ev.read("test") as e:
            specs = e.all_specs()

        manifest, config = get_manifest_and_config(name)

        # without a base image, we should have one layer per spec
        assert len(manifest["layers"]) == len(specs)

        # Now create yet another tag, but with just a single selected spec as root. This should
        # also test the case where Spack doesn't have to upload any binaries, it just has to create
        # a new tag.
        libelf = next(s for s in specs if s.name == "libelf")
        with ev.read("test"):
            # Get libelf spec
            buildcache("push", "--tag", "single_spec", "oci-test", libelf.format("libelf{/hash}"))

        name = ImageReference.from_string("example.com/image:single_spec")
        manifest, config = get_manifest_and_config(name)
        assert len(manifest["layers"]) == 1


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

        # Check that the media type is OCI
        assert retrieved_manifest["mediaType"] == "application/vnd.oci.image.manifest.v1+json"
        assert (
            retrieved_manifest["config"]["mediaType"] == "application/vnd.oci.image.config.v1+json"
        )

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
            assert layer["mediaType"] == "application/vnd.oci.image.layer.v1.tar+gzip"


def test_uploading_with_base_image_in_docker_image_manifest_v2_format(
    tmp_path: pathlib.Path, mutable_database, disable_parallel_buildcache_push
):
    """If the base image uses an old manifest schema, Spack should also use that.
    That is necessary for container images to work with Apptainer, which is rather strict about
    mismatching manifest/layer types."""

    registry_src = InMemoryOCIRegistry("src.example.com")
    registry_dst = InMemoryOCIRegistry("dst.example.com")

    base_image = ImageReference.from_string("src.example.com/my-base-image:latest")

    with oci_servers(registry_src, registry_dst):
        mirror("add", "oci-test", "oci://dst.example.com/image")

        # Create a dummy base image (blob, config, manifest) in registry A in the Docker Image
        # Manifest V2 format.
        rootfs = tmp_path / "rootfs"
        (rootfs / "bin").mkdir(parents=True)
        (rootfs / "bin" / "sh").write_text("hello world")
        tarball = tmp_path / "base.tar.gz"
        with gzip_compressed_tarfile(tarball) as (tar, tar_gz_checksum, tar_checksum):
            tar.add(rootfs, arcname=".")
        tar_gz_digest = Digest.from_sha256(tar_gz_checksum.hexdigest())
        tar_digest = Digest.from_sha256(tar_checksum.hexdigest())
        upload_blob(base_image, str(tarball), tar_gz_digest)
        config = {
            "created": "2015-10-31T22:22:56.015925234Z",
            "author": "Foo <example@example.com>",
            "architecture": "amd64",
            "os": "linux",
            "config": {
                "User": "foo",
                "Memory": 2048,
                "MemorySwap": 4096,
                "CpuShares": 8,
                "ExposedPorts": {"8080/tcp": {}},
                "Env": ["PATH=/usr/bin:/bin"],
                "Entrypoint": ["/bin/sh"],
                "Cmd": ["-c", "'echo hello world'"],
                "Volumes": {"/x": {}},
                "WorkingDir": "/",
            },
            "rootfs": {"diff_ids": [str(tar_digest)], "type": "layers"},
            "history": [
                {
                    "created": "2015-10-31T22:22:54.690851953Z",
                    "created_by": "/bin/sh -c #(nop) ADD file:a3bc1e842b69636f9df5256c49c5374fb4eef1e281fe3f282c65fb853ee171c5 in /",
                }
            ],
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config))
        config_digest = Digest.from_sha256(hashlib.sha256(config_file.read_bytes()).hexdigest())
        upload_blob(base_image, str(config_file), config_digest)
        manifest = {
            "schemaVersion": 2,
            "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
            "config": {
                "mediaType": "application/vnd.docker.container.image.v1+json",
                "size": config_file.stat().st_size,
                "digest": str(config_digest),
            },
            "layers": [
                {
                    "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
                    "size": tarball.stat().st_size,
                    "digest": str(tar_gz_digest),
                }
            ],
        }
        upload_manifest(base_image, manifest)

        # Finally upload some package to registry B with registry A's image as base
        buildcache("push", "--base-image", str(base_image), "oci-test", "mpileaks^mpich")

    # Should have some manifests uploaded to registry B now.
    assert registry_dst.manifests

    # Verify that all manifest are in the Docker Image Manifest V2 format, not OCI.
    # And also check that we're not using annotations, which is an OCI-only "feature".
    for m in registry_dst.manifests.values():
        assert m["mediaType"] == "application/vnd.docker.distribution.manifest.v2+json"
        assert m["config"]["mediaType"] == "application/vnd.docker.container.image.v1+json"
        for layer in m["layers"]:
            assert layer["mediaType"] == "application/vnd.docker.image.rootfs.diff.tar.gzip"
        assert "annotations" not in m
