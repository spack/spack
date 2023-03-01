# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from six import iteritems

from spack.package import *


class Rust(Package):
    """The Rust programming language toolchain

    This package can bootstrap any version of the Rust compiler since Rust
    1.23. It does this by downloading the platform-appropriate binary
    distribution of the desired version of the rust compiler, and then building
    that compiler from source.
    """

    homepage = "https://www.rust-lang.org"
    url = "https://static.rust-lang.org/dist/rustc-1.42.0-src.tar.gz"
    git = "https://github.com/rust-lang/rust.git"

    maintainers("AndrewGaspar")

    phases = ["configure", "build", "install"]

    extendable = True

    variant("rustfmt", default=True, description="Formatting tool for Rust code")

    variant(
        "analysis",
        default=True,
        description="Outputs code analysis that can be consumed by other tools",
    )

    variant("clippy", default=True, description="Linting tool for Rust")

    variant(
        "rls",
        default=False,
        description="The Rust Language Server can be used for IDE integration",
    )

    variant("src", default=True, description="Install Rust source files")
    variant(
        "extra_targets",
        default="none",
        multi=True,
        description="Triples for extra targets to enable. For supported targets, see: https://doc.rust-lang.org/nightly/rustc/platform-support.html",
    )

    depends_on("python@2.7:", type="build")
    depends_on("gmake@3.81:", type="build")
    depends_on("cmake@3.4.3:", type="build")
    depends_on("ninja", when="@1.48.0:", type="build")
    depends_on("pkgconfig", type="build")
    # TODO: openssl@3.x should be supported in later versions
    depends_on("openssl@:1")
    depends_on("libssh2")
    # https://github.com/rust-lang/cargo/issues/10446
    depends_on("libgit2@:1.3", when="@0:1.60")
    depends_on("libgit2")

    # Pre-release Versions
    version("master", branch="master", submodules=True)

    # These version strings are officially supported, but aren't explicitly
    # listed because there's no stable checksum for them.
    version("nightly")
    # version('beta')

    # Version Notes:
    # Here's some information on why your favorite Rust version may be missing.
    #
    # < 1.23:
    # Rust seems to eagerly search for ar next to cc. Spack makes wrappers for
    # cc and c++, but not for ar, so no ar is found. In future versions, ar
    # can be specified in the config.
    #
    # < 1.17:
    # The `x.py` bootstrapping script did not exist prior to Rust 1.17. It
    # would be possible to support both, but for simplicitly, we only support
    # Rust 1.17 and newer
    version("1.65.0", sha256="5828bb67f677eabf8c384020582b0ce7af884e1c84389484f7f8d00dd82c0038")
    version("1.60.0", sha256="20ca826d1cf674daf8e22c4f8c4b9743af07973211c839b85839742314c838b7")
    version("1.58.1", sha256="a839afdd3625d6f3f3c4c10b79813675d1775c460d14be1feaf33a6c829c07c7")
    version("1.51.0", sha256="7a6b9bafc8b3d81bbc566e7c0d1f17c9f499fd22b95142f7ea3a8e4d1f9eb847")
    version("1.48.0", sha256="0e763e6db47d5d6f91583284d2f989eacc49b84794d1443355b85c58d67ae43b")
    version("1.47.0", sha256="3185df064c4747f2c8b9bb8c4468edd58ff4ad6d07880c879ac1b173b768d81d")
    version("1.46.0", sha256="2d6a3b7196db474ba3f37b8f5d50a1ecedff00738d7846840605b42bfc922728")
    version("1.45.1", sha256="ea53e6424e3d1fe56c6d77a00e72c5d594b509ec920c5a779a7b8e1dbd74219b")
    version("1.44.1", sha256="7e2e64cb298dd5d5aea52eafe943ba0458fa82f2987fdcda1ff6f537b6f88473")
    version("1.44.0", sha256="bf2df62317e533e84167c5bc7d4351a99fdab1f9cd6e6ba09f51996ad8561100")

    # The Rust bootstrapping process requires a bootstrapping compiler. The
    # easiest way to do this is to download the binary distribution of the
    # same version of the compiler and build with that.
    #
    # This dictionary contains a version: hash dictionary for each supported
    # Rust target.
    rust_releases = {
        "1.65.0": {
            "x86_64-unknown-linux-gnu": "8f754fdd5af783fe9020978c64e414cb45f3ad0a6f44d045219bbf2210ca3cb9",
            "powerpc64le-unknown-linux-gnu": "3f1d0d5bb13213348dc65e373f8c412fc0a12ee55abc1c864f7e0300932fc687",
            "aarch64-unknown-linux-gnu": "f406136010e6a1cdce3fb6573506f00d23858af49dd20a46723c3fa5257b7796",
            "x86_64-apple-darwin": "139087a3937799415fd829e5a88162a69a32c23725a44457f9c96b98e4d64a7c",
            "aarch64-apple-darwin": "7ddc335bd10fc32d3039ef36248a5d0c4865db2437c8aad20a2428a6cf41df09",
        },
        "1.60.0": {
            "x86_64-unknown-linux-gnu": "b8a4c3959367d053825e31f90a5eb86418eb0d80cacda52bfa80b078e18150d5",
            "powerpc64le-unknown-linux-gnu": "80125e90285b214c2b1f56ab86a09c8509aa17aec9d7127960a86a7008e8f7de",
            "aarch64-unknown-linux-gnu": "99c419c2f35d4324446481c39402c7baecd7a8baed7edca9f8d6bbd33c05550c",
            "x86_64-apple-darwin": "0b10dc45cddc4d2355e38cac86d71a504327cb41d41d702d4050b9847ad4258c",
            "aarch64-apple-darwin": "b532672c278c25683ca63d78e82bae829eea1a32308e844954fb66cfe34ad222",
        },
        "1.58.1": {
            "x86_64-unknown-linux-gnu": "4fac6df9ea49447682c333e57945bebf4f9f45ec7b08849e507a64b2ccd5f8fb",
            "powerpc64le-unknown-linux-gnu": "b15baef702cbd6f0ea2bef7bf98ca7ce5644f2beb219028e8a12e7053da4c849",
            "aarch64-unknown-linux-gnu": "ce557516593e4526709b0f33c2e1d7c932b3ddf76af94c2417d8d667921ce90c",
            "x86_64-apple-darwin": "d0044680fc132a721481b130a0a4282a444867f423efdb890fe13e447966412f",
        },
        "1.51.0": {
            "x86_64-unknown-linux-gnu": "9e125977aa13f012a68fdc6663629c685745091ae244f0587dd55ea4e3a3e42f",
            "powerpc64le-unknown-linux-gnu": "7362f561104d7be4836507d3a53cd39444efcdf065813d559beb1f54ce9f7680",
            "aarch64-unknown-linux-gnu": "fd31c78fffad52c03cac5a7c1ee5db3f34b2a77d7bc862707c0f71e209180a84",
            "x86_64-apple-darwin": "765212098a415996b767d1e372ce266caf94027402b269fec33291fffc085ca4",
        },
        "1.48.0": {
            "x86_64-unknown-linux-gnu": "950420a35b2dd9091f1b93a9ccd5abc026ca7112e667f246b1deb79204e2038b",
            "powerpc64le-unknown-linux-gnu": "e6457a0214f3b1b04bd5b2618bba7e3826e254216420dede2971b571a1c13bb1",
            "aarch64-unknown-linux-gnu": "c4769418d8d89f432e4a3a21ad60f99629e4b13bbfc29aef7d9d51c4e8ee8a8a",
            "x86_64-apple-darwin": "f30ce0162b39dc7cf877020cec64d4826cad50467af493d180b5b28cf5eb50b3",
        },
        "1.47.0": {
            "x86_64-unknown-linux-gnu": "d0e11e1756a072e8e246b05d54593402813d047d12e44df281fbabda91035d96",
            "powerpc64le-unknown-linux-gnu": "5760c3b1897ea70791320c2565f3eef700a3d54059027b84bbe6b8d6157f81c8",
            "aarch64-unknown-linux-gnu": "753c905e89a714ab9bce6fe1397b721f29c0760c32f09d2f328af3d39919c8e6",
            "x86_64-apple-darwin": "84e5be6c5c78734deba911dcf80316be1e4c7da2c59413124d039ad96620612f",
        },
        "1.46.0": {
            "x86_64-unknown-linux-gnu": "e3b98bc3440fe92817881933f9564389eccb396f5f431f33d48b979fa2fbdcf5",
            "powerpc64le-unknown-linux-gnu": "89e2f4761d257f017a4b6aa427f36ac0603195546fa2cfded8c899789832941c",
            "aarch64-unknown-linux-gnu": "f0c6d630f3dedb3db69d69ed9f833aa6b472363096f5164f1068c7001ca42aeb",
            "x86_64-apple-darwin": "82d61582a3772932432a99789c3b3bd4abe6baca339e355048ca9efb9ea5b4db",
        },
        "1.45.1": {
            "x86_64-unknown-linux-gnu": "76dc9f05b3bfd0465d6e6d22bc9fd5db0b473e3548e8b3d266ecfe4d9e5dca16",
            "powerpc64le-unknown-linux-gnu": "271846e4f5adc9a33754794c2ffab851f9e0313c8c1315264e7db5c8f63ab7ab",
            "aarch64-unknown-linux-gnu": "d17fd560e8d5d12304835b71a7e22ac2c3babf4b9768db6a0e89868b4444f728",
            "x86_64-apple-darwin": "7334c927e4d2d12d209bf941b97ba309e548413e241d2d263c39c6e12b3ce154",
        },
        "1.44.1": {
            "x86_64-unknown-linux-gnu": "a41df89a461a580536aeb42755e43037556fba2e527dd13a1e1bb0749de28202",
            "powerpc64le-unknown-linux-gnu": "22deeca259459db31065af7c862fcab7fbfb623200520c65002ed2ba93d87ad2",
            "aarch64-unknown-linux-gnu": "a2d74ebeec0b6778026b6c37814cdc91d14db3b0d8b6d69d036216f4d9cf7e49",
            "x86_64-apple-darwin": "a5464e7bcbce9647607904a4afa8362382f1fc55d39e7bbaf4483ac00eb5d56a",
        },
        "1.44.0": {
            "x86_64-unknown-linux-gnu": "eaa34271b4ac4d2c281831117d4d335eed0b37fe7a34477d9855a6f1d930a624",
            "powerpc64le-unknown-linux-gnu": "97038ea935c7a5b21f5aaaaad409c514e2b2ae8ea55994ba39645f453e98bc9f",
            "aarch64-unknown-linux-gnu": "bcc916003cb9c7ff44f5f9af348020b422dbc5bd4fe49bdbda2de6ce0a1bb745",
            "x86_64-apple-darwin": "f20388b80b2b0a8b122d89058f785a2cf3b14e93bcac53471d60fdb4106ffa35",
        },
    }

    # This dictionary maps Rust target architectures to Spack constraints that
    # match that target.
    rust_archs = {
        "x86_64-unknown-linux-gnu": [
            {"platform": "linux", "target": "x86_64:"},
            {"platform": "cray", "target": "x86_64:"},
        ],
        "powerpc64le-unknown-linux-gnu": [
            {"platform": "linux", "target": "ppc64le:"},
            {"platform": "cray", "target": "ppc64le:"},
        ],
        "aarch64-unknown-linux-gnu": [
            {"platform": "linux", "target": "aarch64:"},
            {"platform": "cray", "target": "aarch64:"},
        ],
        "x86_64-apple-darwin": [{"platform": "darwin", "target": "x86_64:"}],
        "aarch64-apple-darwin": [{"platform": "darwin", "target": "aarch64:"}],
    }

    # Specifies the strings which represent a pre-release Rust version. These
    # always bootstrap with the latest beta release.
    #
    # NOTE: These are moving targets, and therefore have no stable checksum. Be
    # sure to specify "-n" or "--no-checksum" when installing these versions.
    rust_prerelease_versions = ["beta", "nightly", "master"]

    for prerelease_version in rust_prerelease_versions:
        for rust_target, rust_arch_list in iteritems(rust_archs):
            for rust_arch in rust_arch_list:
                # All pre-release builds are built with the latest beta
                # compiler.
                resource(
                    name="rust-beta-{target}".format(target=rust_target),
                    url="https://static.rust-lang.org/dist/rust-beta-{target}.tar.gz".format(
                        target=rust_target
                    ),
                    # Fake SHA - checksums should never be checked for
                    # pre-release builds, anyway
                    sha256="0000000000000000000000000000000000000000000000000000000000000000",
                    destination="spack_bootstrap_stage",
                    when="@{version} platform={platform} target={target}".format(
                        version=prerelease_version,
                        platform=rust_arch["platform"],
                        target=rust_arch["target"],
                    ),
                )

    # This loop generates resources for each binary distribution, and maps
    # them to the version of the compiler they bootstrap. This is in place
    # of listing each resource explicitly, which would be potentially even
    # more verbose.
    #
    # NOTE: This loop should technically specify the architecture to be the
    # _host_ architecture, not the target architecture, in order to support
    # cross compiling. I'm not sure Spack provides a way to specify a
    # distinction in the when clause, though.
    for rust_version, rust_targets in iteritems(rust_releases):
        for rust_target, rust_sha256 in iteritems(rust_targets):
            for rust_arch in rust_archs[rust_target]:
                resource(
                    name="rust-{version}-{target}".format(
                        version=rust_version, target=rust_target
                    ),
                    url="https://static.rust-lang.org/dist/rust-{version}-{target}.tar.gz".format(
                        version=rust_version, target=rust_target
                    ),
                    sha256=rust_sha256,
                    destination="spack_bootstrap_stage",
                    when="@{ver} platform={platform} target={target}".format(
                        ver=rust_version,
                        platform=rust_arch["platform"],
                        target=rust_arch["target"],
                    ),
                )

    executables = ["^rustc$"]

    @classmethod
    def determine_version(csl, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.match(r"rustc (\S+)", output)
        return match.group(1) if match else None

    # This routine returns the target architecture we intend to build for.
    def get_rust_target(self):
        if "platform=linux" in self.spec or "platform=cray" in self.spec:
            if "target=x86_64:" in self.spec:
                return "x86_64-unknown-linux-gnu"
            elif "target=ppc64le:" in self.spec:
                return "powerpc64le-unknown-linux-gnu"
            elif "target=aarch64:" in self.spec:
                return "aarch64-unknown-linux-gnu"
        elif "platform=darwin" in self.spec:
            if "target=x86_64:" in self.spec:
                return "x86_64-apple-darwin"
            elif "target=aarch64:" in self.spec:
                return "aarch64-apple-darwin"

        raise InstallError("rust is not supported for '{0}'".format(self.spec.architecture))

    def check_newer(self, version):
        if "@master" in self.spec or "@beta" in self.spec or "@nightly" in self.spec:
            return True

        return "@{0}:".format(version) in self.spec

    def patch(self):
        if self.spec.satisfies("@1.51.0"):
            # see 31c93397bde7 upstream
            filter_file(
                "panic!(out);", 'panic!("{}", out);', "src/bootstrap/builder.rs", string=True
            )

    def configure(self, spec, prefix):
        target = self.get_rust_target()

        # Bootstrapping compiler selection:
        # Pre-release compilers use the latest beta release for the
        # bootstrapping compiler.
        # Versioned releases bootstrap themselves.
        if "@beta" in spec or "@nightly" in spec or "@master" in spec:
            bootstrap_version = "beta"
        else:
            bootstrap_version = spec.version
        # See the NOTE above the resource loop - should be host architecture,
        # not target aarchitecture if we're to support cross-compiling.
        bootstrapping_install = Executable(
            "./spack_bootstrap_stage/rust-{version}-{target}/install.sh".format(
                version=bootstrap_version, target=target
            )
        )
        # install into the staging area
        bootstrapping_install(
            "--prefix={0}".format(join_path(self.stage.source_path, "spack_bootstrap"))
        )

        boot_bin = join_path(self.stage.source_path, "spack_bootstrap/bin")

        # Always build rustc and cargo
        tools = ["rustc", "cargo"]
        # Only make additional components available in 'rust-bootstrap'
        if "+rustfmt" in self.spec:
            tools.append("rustfmt")
        if "+analysis" in self.spec:
            tools.append("analysis")
        if "@1.33: +clippy" in self.spec:
            tools.append("clippy")
        if "+rls" in self.spec:
            tools.append("rls")
        if "+src" in self.spec:
            tools.append("src")

        ar = which("ar", required=True)

        extra_targets = []
        if not self.spec.satisfies("extra_targets=none"):
            extra_targets = list(self.spec.variants["extra_targets"].value)

        targets = [self.get_rust_target()] + extra_targets
        target_spec = "target=[" + ",".join('"{0}"'.format(target) for target in targets) + "]"
        target_specs = "\n".join(
            '[target.{0}]\nar = "{1}"\n'.format(target, ar.path) for target in targets
        )

        # build.tools was introduced in Rust 1.25
        tools_spec = "tools={0}".format(tools) if self.check_newer("1.25") else ""
        # This is a temporary fix due to rust 1.42 breaking self bootstrapping
        # See: https://github.com/rust-lang/rust/issues/69953
        #
        # In general, this should be safe because bootstrapping typically
        # ensures everything but the bootstrapping script is warning free for
        # the latest set of warning.
        deny_warnings_spec = "deny-warnings = false" if "@1.42.0" in self.spec else ""

        # "Nightly" and master builds want a path to rustfmt - otherwise, it
        # will try to download rustfmt from the Internet. We'll give it rustfmt
        # for the bootstrapping compiler, but it ultimately shouldn't matter
        # because this package never invokes it. To be clear, rustfmt from the
        # bootstrapping compiler is probably incorrect. See: src/stage0.txt in
        # Rust to see what the current "official" rustfmt version for Rust is.
        if "@master" in spec or "@nightly" in spec:
            rustfmt_spec = 'rustfmt="{0}"'.format(join_path(boot_bin, "rustfmt"))
        else:
            rustfmt_spec = ""

        with open("config.toml", "w") as out_file:
            out_file.write(
                """\
[build]
cargo = "{cargo}"
rustc = "{rustc}"
docs = false
vendor = true
extended = true
verbose = 2
{target_spec}
{tools_spec}
{rustfmt_spec}

[rust]
channel = "stable"
rpath = true
{deny_warnings_spec}

{target_specs}

[install]
prefix = "{prefix}"
sysconfdir = "etc"
""".format(
                    cargo=join_path(boot_bin, "cargo"),
                    rustc=join_path(boot_bin, "rustc"),
                    prefix=prefix,
                    deny_warnings_spec=deny_warnings_spec,
                    target_spec=target_spec,
                    target_specs=target_specs,
                    tools_spec=tools_spec,
                    rustfmt_spec=rustfmt_spec,
                )
            )

    def build(self, spec, prefix):
        python(
            "./x.py",
            "build",
            extra_env={
                # vendored libgit2 wasn't correctly building (couldn't find the
                # vendored libssh2), so let's just have spack build it
                "LIBSSH2_SYS_USE_PKG_CONFIG": "1",
                "LIBGIT2_SYS_USE_PKG_CONFIG": "1",
            },
        )

    def install(self, spec, prefix):
        python("./x.py", "install")
