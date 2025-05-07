# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *

_is_macos = sys.platform == "darwin"


def write_containers_conf(pkg_obj, pkgs: list[str]):
    # podman requires its runtime deps to be in a configured directory
    # https://github.com/containers/common/blob/main/docs/containers.conf.5.md
    # we choose the user-friendly option of CONTAINERS_CONF_OVERRIDE, which respects
    # existing configurations set by the user
    helper_dirs = ", ".join(f'"{x}"' for x in [pkg_obj.spec[pkg].prefix.bin for pkg in pkgs])

    config = f"""
    [engine]

    helper_binaries_dir=[{helper_dirs}]
    """

    with open(join_path(pkg_obj.prefix, "containers.conf"), "w") as f:
        f.write(config)


class Podman(Package):
    """An optionally rootless and daemonless container engine: alias docker=podman"""

    homepage = "https://podman.io"
    url = "https://github.com/containers/podman/archive/refs/tags/v4.3.1.tar.gz"
    maintainers("alecbcs")

    license("Apache-2.0")

    version("5.4.2", sha256="8da62c25956441b14d781099e803e38410a5753e5c7349bcd34615b9ca5ed4f2")
    version("4.9.3", sha256="37afc5bba2738c68dc24400893b99226c658cc9a2b22309f4d7abe7225d8c437")
    version("4.8.3", sha256="3a99b6c82644fa52929cf4143943c63d6784c84094892bc0e14197fa38a1c7fa")
    version("4.7.2", sha256="10346c5603546427bd809b4d855d1e39b660183232309128ad17a64969a0193d")
    version("4.6.2", sha256="2d8e04f0c3819c3f0ed1ca5d01da87e6d911571b96ae690448f7f75df41f2ad1")
    version("4.5.1", sha256="ee2c8b02b7fe301057f0382637b995a9c6c74e8d530692d6918e4c509ade6e39")
    version("4.3.1", sha256="455c29c4ee78cd6365e5d46e20dd31a5ce4e6e1752db6774253d76bd3ca78813")
    version("3.4.7", sha256="4af6606dd072fe946960680611ba65201be435b43edbfc5cc635b2a01a899e6e")
    version("3.4.2", sha256="b0c4f9a11eb500b1d440d5e51a6c0c632aa4ac458e2dc0362f50f999eb7fbf31")

    depends_on("c", type="build")  # generated

    requires(
        "@5.4.2:",
        when="platform=darwin",
        msg="podman for macOS is only supported on version 5.4.2 and above.",
    )

    # see https://github.com/containers/podman/issues/22121
    if _is_macos and macos_version() < Version("13"):
        raise InstallError("podman for macOS requires Ventura or later")

    # See <https://github.com/containers/podman/issues/16996> for the
    # respective issue and the suggested patch
    # issue was fixed as of 4.4.0
    patch("markdown-utf8.diff", when="@4:4.3.1")

    # universal deps
    depends_on("go@1.22.8:", type="build", when="@5.4.2:")
    depends_on("go", type="build")
    depends_on("go-md2man", type="build")
    depends_on("gmake", type="build")

    # linux deps
    with when("platform=linux"):
        depends_on("pkgconfig", type="build")
        depends_on("cni-plugins", type="run")
        depends_on("conmon", type="run")
        depends_on("runc", type="run")
        depends_on("slirp4netns", type="run")
        depends_on("passt", type="run", when="@5.4.2:")
        depends_on("gpgme")
        depends_on("libassuan")
        depends_on("libgpg-error")
        depends_on("libseccomp")

    with when("platform=darwin"):
        # for context on the dependencies (strictness of version constraints), see
        # https://github.com/containers/podman/blob/#{version}/contrib/pkginstaller/Makefile
        # via https://github.com/Homebrew/homebrew-core/blob/master/Formula/p/podman.rb
        depends_on("gvproxy@0.8.4", type="run", when="@5.4.2")
        depends_on("vfkit@0.6.0", type="run", when="@5.4.2")

    @when("platform=linux")
    def patch(self):
        defs = FileFilter("vendor/github.com/containers/common/pkg/config/default.go")

        # Prepend the provided runc executable to podman's built-in runc search path
        defs.filter('"runc": {', '"runc": {' + '"{0}",'.format(self.spec["runc"].prefix.sbin.runc))
        # Prepend the provided conmon executable to podman's built-in conmon search path
        defs.filter(
            r"ConmonPath = \[\]string{",
            "ConmonPath = []string{"
            + '\n        "{0}",'.format(self.spec["conmon"].prefix.bin.conmon),
        )
        # Prepend the provided cni-plugins directory to the cni-plugin search path
        defs.filter(
            r"DefaultCNIPluginDirs = \[\]string{",
            "DefaultCNIPluginDirs = []string{"
            + '\n        "{0}",'.format(self.spec["cni-plugins"].prefix.bin),
        )
        # Set the default path for slirp4netns to the provided slirp4netns executable
        defs.filter(
            "cniConfig := _cniConfigDir",
            "cniConfig := _cniConfigDir"
            + '\n        defaultEngineConfig.NetworkCmdPath = "{0}"'.format(
                self.spec["slirp4netns"].prefix.bin.slirp4netns
            ),
        )
        # Use the podman install prefix as fallback path for finding container.conf
        filter_file(
            r"/usr", self.prefix, "vendor/github.com/containers/common/pkg/config/config.go"
        )

    @when("platform=darwin")
    def install(self, spec, prefix):
        # macos-specific installation
        # ported from the homebrew formula
        mkdirp(prefix.bin)
        make("podman-remote")
        make("podman-mac-helper")
        install("bin/darwin/podman", prefix.bin)
        install("bin/darwin/podman-mac-helper", prefix.bin)

        write_containers_conf(self, ["gvproxy", "vfkit"])

    @when("@5.4.2:")
    def setup_run_environment(self, env):
        # needs to be set any time a user loads the package
        env.set("CONTAINERS_CONF_OVERRIDE", join_path(self.prefix, "containers.conf"))

    @when("platform=linux")
    def install(self, spec, prefix):
        # Set default policy.json to be located in the install prefix (documented)
        env["EXTRA_LDFLAGS"] = (
            "-X github.com/containers/image/v5/signature.systemDefaultPolicyPath="
            + prefix
            + "/etc/containers/policy.json"
        )
        # Build and installation needs to be in two separate make calls
        # The devicemapper and btrfs drivers are (so far) not enabled in this recipe
        tags = "seccomp exclude_graphdriver_devicemapper exclude_graphdriver_btrfs cni"
        make("-e", "BUILDTAGS=" + tags)
        make("install", "PREFIX=" + prefix)
        # Install an initial etc/containers/policy.json (configured in prefix above)
        mkdirp(prefix.etc.containers)
        install("test/policy.json", prefix.etc.containers)
        # Cleanup directory trees which are created as part of the go build process
        remove_linked_tree(prefix.src)
        remove_linked_tree(prefix.pkg)

        write_containers_conf(self, ["passt"])
