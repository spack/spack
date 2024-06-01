# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re
import sys

from llnl.util.filesystem import windows_sfn

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.nmake import NMakeBuilder
from spack.package import *

is_windows = sys.platform == "win32"


class Curl(NMakePackage, AutotoolsPackage):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "https://curl.se/"
    # URL must remain http:// so Spack can bootstrap curl
    url = "http://curl.haxx.se/download/curl-7.78.0.tar.bz2"

    executables = ["^curl$"]
    tags = ["build-tools", "windows"]

    maintainers("alecbcs")

    license("curl")

    version("8.7.1", sha256="05bbd2b698e9cfbab477c33aa5e99b4975501835a41b7ca6ca71de03d8849e76")
    version("8.6.0", sha256="b4785f2d8877fa92c0e45d7155cf8cc6750dbda961f4b1a45bcbec990cf2fa9b")
    version("8.4.0", sha256="e5250581a9c032b1b6ed3cf2f9c114c811fc41881069e9892d115cc73f9e88c6")

    # Deprecated versions due to CVEs
    # CVE-2023-38545
    version(
        "8.1.2",
        sha256="b54974d32fd610acace92e3df1f643144015ac65847f0a041fdc17db6f43f243",
        deprecated=True,
    )
    version(
        "8.0.1",
        sha256="9b6b1e96b748d04b968786b6bdf407aa5c75ab53a3d37c1c8c81cdb736555ccf",
        deprecated=True,
    )
    version(
        "7.88.1",
        sha256="8224b45cce12abde039c12dc0711b7ea85b104b9ad534d6e4c5b4e188a61c907",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2022-43551
    version(
        "7.87.0",
        sha256="5d6e128761b7110946d1276aff6f0f266f2b726f5e619f7e0a057a474155f307",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2022-32221
    version(
        "7.86.0",
        sha256="f5ca69db03eea17fa8705bdfb1a9f58d76a46c9010518109bb38f313137e0a28",
        deprecated=True,
    )
    version(
        "7.85.0",
        sha256="21a7e83628ee96164ac2b36ff6bf99d467c7b0b621c1f7e317d8f0d96011539c",
        deprecated=True,
    )
    version(
        "7.84.0",
        sha256="702fb26e73190a3bd77071aa146f507b9817cc4dfce218d2ab87f00cd3bc059d",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2022-32206
    version(
        "7.83.0",
        sha256="247c7ec7521c4258e65634e529270d214fe32969971cccb72845e7aa46831f96",
        deprecated=True,
    )
    version(
        "7.82.0",
        sha256="46d9a0400a33408fd992770b04a44a7434b3036f2e8089ac28b57573d59d371f",
        deprecated=True,
    )
    version(
        "7.81.0",
        sha256="1e7a38d7018ec060f1f16df839854f0889e94e122c4cfa5d3a37c2dc56f1e258",
        deprecated=True,
    )
    version(
        "7.80.0",
        sha256="dd0d150e49cd950aff35e16b628edf04927f0289df42883750cf952bb858189c",
        deprecated=True,
    )
    version(
        "7.79.1",
        sha256="de62c4ab9a9316393962e8b94777a570bb9f71feb580fb4475e412f2f9387851",
        deprecated=True,
    )
    version(
        "7.79.0",
        sha256="d607a677f473f79f96c964100327125a6204a39d835dc00dab7fc0129b959f42",
        deprecated=True,
    )
    version(
        "7.78.0",
        sha256="98530b317dc95ccb324bbe4f834f07bb642fbc393b794ddf3434f246a71ea44a",
        deprecated=True,
    )
    version(
        "7.77.0",
        sha256="6c0c28868cb82593859fc43b9c8fdb769314c855c05cf1b56b023acf855df8ea",
        deprecated=True,
    )
    version(
        "7.76.1",
        sha256="7a8e184d7d31312c4ebf6a8cb59cd757e61b2b2833a9ed4f9bf708066e7695e9",
        deprecated=True,
    )
    version(
        "7.76.0",
        sha256="e29bfe3633701590d75b0071bbb649ee5ca4ca73f00649268bd389639531c49a",
        deprecated=True,
    )
    version(
        "7.75.0",
        sha256="50552d4501c178e4cc68baaecc487f466a3d6d19bbf4e50a01869effb316d026",
        deprecated=True,
    )
    version(
        "7.74.0",
        sha256="0f4d63e6681636539dc88fa8e929f934cd3a840c46e0bf28c73be11e521b77a5",
        deprecated=True,
    )
    version(
        "7.73.0",
        sha256="cf34fe0b07b800f1c01a499a6e8b2af548f6d0e044dca4a29d88a4bee146d131",
        deprecated=True,
    )
    version(
        "7.72.0",
        sha256="ad91970864102a59765e20ce16216efc9d6ad381471f7accceceab7d905703ef",
        deprecated=True,
    )
    version(
        "7.71.0",
        sha256="600f00ac2481a89548a4141ddf983fd9386165e1960bac91d0a1c81dca5dd341",
        deprecated=True,
    )
    version(
        "7.68.0",
        sha256="207f54917dd6a2dc733065ccf18d61bb5bebeaceb5df49cd9445483e8623eeb9",
        deprecated=True,
    )
    version(
        "7.64.0",
        sha256="d573ba1c2d1cf9d8533fadcce480d778417964e8d04ccddcc76e591d544cf2eb",
        deprecated=True,
    )
    version(
        "7.63.0",
        sha256="9bab7ed4ecff77020a312d84cc5fb7eb02d58419d218f267477a724a17fd8dd8",
        deprecated=True,
    )
    version(
        "7.60.0",
        sha256="897dfb2204bd99be328279f88f55b7c61592216b0542fcbe995c60aa92871e9b",
        deprecated=True,
    )
    version(
        "7.59.0",
        sha256="b5920ffd6a8c95585fb95070e0ced38322790cb335c39d0dab852d12e157b5a0",
        deprecated=True,
    )
    version(
        "7.56.0",
        sha256="de60a4725a3d461c70aa571d7d69c788f1816d9d1a8a2ef05f864ce8f01279df",
        deprecated=True,
    )
    version(
        "7.54.0",
        sha256="f50ebaf43c507fa7cc32be4b8108fa8bbd0f5022e90794388f3c7694a302ff06",
        deprecated=True,
    )
    version(
        "7.53.1",
        sha256="1c7207c06d75e9136a944a2e0528337ce76f15b9ec9ae4bb30d703b59bf530e8",
        deprecated=True,
    )
    version(
        "7.52.1",
        sha256="d16185a767cb2c1ba3d5b9096ec54e5ec198b213f45864a38b3bda4bbf87389b",
        deprecated=True,
    )
    version(
        "7.50.3",
        sha256="7b7347d976661d02c84a1f4d6daf40dee377efdc45b9e2c77dedb8acf140d8ec",
        deprecated=True,
    )
    version(
        "7.50.2",
        sha256="0c72105df4e9575d68bcf43aea1751056c1d29b1040df6194a49c5ac08f8e233",
        deprecated=True,
    )
    version(
        "7.50.1",
        sha256="3c12c5f54ccaa1d40abc65d672107dcc75d3e1fcb38c267484334280096e5156",
        deprecated=True,
    )
    version(
        "7.49.1",
        sha256="eb63cec4bef692eab9db459033f409533e6d10e20942f4b060b32819e81885f1",
        deprecated=True,
    )
    version(
        "7.47.1",
        sha256="ddc643ab9382e24bbe4747d43df189a0a6ce38fcb33df041b9cb0b3cd47ae98f",
        deprecated=True,
    )
    version(
        "7.46.0",
        sha256="b7d726cdd8ed4b6db0fa1b474a3c59ebbbe4dcd4c61ac5e7ade0e0270d3195ad",
        deprecated=True,
    )
    version(
        "7.45.0",
        sha256="65154e66b9f8a442b57c436904639507b4ac37ec13d6f8a48248f1b4012b98ea",
        deprecated=True,
    )
    version(
        "7.44.0",
        sha256="1e2541bae6582bb697c0fbae49e1d3e6fad5d05d5aa80dbd6f072e0a44341814",
        deprecated=True,
    )
    version(
        "7.43.0",
        sha256="baa654a1122530483ccc1c58cc112fec3724a82c11c6a389f1e6a37dc8858df9",
        deprecated=True,
    )
    version(
        "7.42.1",
        sha256="e2905973391ec2dfd7743a8034ad10eeb58dab8b3a297e7892a41a7999cac887",
        deprecated=True,
    )

    default_tls = "openssl"
    if sys.platform == "darwin":
        default_tls = "secure_transport"
    elif sys.platform == "win32":
        default_tls = "sspi"

    # TODO: add dependencies for other possible TLS backends
    variant(
        "tls",
        default=default_tls,
        description="TLS backend",
        values=(
            # 'amissl',
            # 'bearssl',
            "gnutls",
            conditional("mbedtls", when="@7.46:"),
            # 'mesalink',
            conditional("nss", when="@:7.81"),
            "openssl",
            # 'rustls',
            # 'schannel',
            "secure_transport",
            # 'wolfssl',
            conditional("sspi", when="platform=windows"),
        ),
        multi=True,
    )
    variant("nghttp2", default=True, description="build nghttp2 library (requires C++11)")
    variant("libssh2", default=False, description="enable libssh2 support")
    variant("libssh", default=False, description="enable libssh support", when="@7.58:")
    variant("gssapi", default=False, description="enable Kerberos support")
    variant("librtmp", default=False, description="enable Rtmp support")
    variant("ldap", default=False, description="enable ldap support")
    variant("libidn2", default=False, description="enable libidn2 support")
    for plat in ["darwin", "linux"]:
        with when("platform=%s" % plat):
            # curl queries pkgconfig for openssl compilation flags
            depends_on("pkgconfig", type="build")
    variant(
        "libs",
        default="shared,static" if not is_windows else "shared",
        values=("shared", "static"),
        multi=not is_windows,
        description="Build shared libs, static libs or both",
    )

    conflicts("platform=linux", when="tls=secure_transport", msg="Only supported on macOS")

    depends_on("gnutls", when="tls=gnutls")
    depends_on("mbedtls@2: +pic", when="@7.79: tls=mbedtls")
    depends_on("mbedtls@:2 +pic", when="@:7.78 tls=mbedtls")
    depends_on("nss", when="tls=nss")

    with when("tls=openssl"):
        depends_on("openssl")
        # Since https://github.com/curl/curl/commit/ee36e86ce8f77a017c49b8312814c33f4b969565
        # there is OpenSSL 3 detection.
        depends_on("openssl@:1", when="@:7.76")

    depends_on("libidn2", when="+libidn2")
    depends_on("zlib-api")
    depends_on("nghttp2", when="+nghttp2")
    depends_on("libssh2", when="+libssh2")
    depends_on("libssh", when="+libssh")
    depends_on("krb5", when="+gssapi")
    depends_on("rtmpdump", when="+librtmp")

    # https://github.com/curl/curl/issues/12832
    # https://github.com/curl/curl/issues/13508
    depends_on("perl", type="build", when="@8.6:8.7.1")

    # https://github.com/curl/curl/pull/9054
    patch("easy-lock-sched-header.patch", when="@7.84.0")

    build_system("autotools", conditional("nmake", when="platform=windows"), default="autotools")

    @classmethod
    def determine_version(cls, exe):
        curl = Executable(exe)
        output = curl("--version", output=str, error=str)
        match = re.match(r"curl ([\d.]+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        for exe in exes:
            variants = ""
            curl = Executable(exe)
            output = curl("--version", output=str, error=str)
            if "nghttp2" in output:
                variants += "+nghttp2"
            protocols_match = re.search(r"Protocols: (.*)\n", output)
            if protocols_match:
                protocols = protocols_match.group(1).strip().split(" ")
                if "ldap" in protocols:
                    variants += "+ldap"
            features_match = re.search(r"Features: (.*)\n", output)
            if features_match:
                features = features_match.group(1).strip().split(" ")
                if "GSS-API" in features:
                    variants += "+gssapi"
            # TODO: Determine TLS backend if needed.
            # TODO: Determine more variants.
            return variants

    @property
    def command(self):
        return Executable(self.prefix.bin.join("curl-config"))

    def flag_handler(self, name, flags):
        build_system_flags = []
        if name == "cflags" and self.spec.compiler.name in ["intel", "oneapi"]:
            build_system_flags = ["-we147"]
        return flags, None, build_system_flags


class BuildEnvironment:
    def setup_dependent_build_environment(self, env, dependent_spec):
        if self.spec.satisfies("libs=static"):
            env.append_flags("CFLAGS", "-DCURL_STATICLIB")
            env.append_flags("CXXFLAGS", "-DCURL_STATICLIB")


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec

        args = [
            "--with-zlib=" + spec["zlib-api"].prefix,
            # Prevent unintentional linking against system libraries: we could
            # add variants for these in the future
            "--without-brotli",
            "--without-libgsasl",
            "--without-libpsl",
            "--without-zstd",
        ]

        args += self.enable_or_disable("libs")

        # Make gnutls / openssl decide what certs are trusted.
        # TODO: certs for other tls options.
        if spec.satisfies("tls=gnutls") or spec.satisfies("tls=openssl"):
            args.extend(["--without-ca-bundle", "--without-ca-path", "--with-ca-fallback"])

        # https://daniel.haxx.se/blog/2021/06/07/bye-bye-metalink-in-curl/
        # We always disable it explicitly, but the flag is gone in newer
        # versions.
        if spec.satisfies("@:7.77"):
            args.append("--without-libmetalink")

        if spec.satisfies("+gssapi"):
            args.append("--with-gssapi=" + spec["krb5"].prefix)
        else:
            args.append("--without-gssapi")

        args += self.with_or_without("tls")
        args += self.with_or_without("libidn2", activation_value="prefix")
        args += self.with_or_without("librtmp")
        args += self.with_or_without("nghttp2", activation_value="prefix")
        args += self.with_or_without("libssh2", activation_value="prefix")
        args += self.with_or_without("libssh", activation_value="prefix")
        args += self.enable_or_disable("ldap")

        return args

    def with_or_without_gnutls(self, activated):
        if activated:
            return "--with-gnutls=" + self.spec["gnutls"].prefix
        else:
            return "--without-gnutls"

    def with_or_without_mbedtls(self, activated):
        if self.spec.satisfies("@7.46:"):
            if activated:
                return "--with-mbedtls=" + self.spec["mbedtls"].prefix
            else:
                return "--without-mbedtls"

    def with_or_without_nss(self, activated):
        if activated:
            return "--with-nss=" + self.spec["nss"].prefix
        else:
            return "--without-nss"

    def with_or_without_openssl(self, activated):
        if self.spec.satisfies("@7.77:"):
            if activated:
                return "--with-openssl=" + self.spec["openssl"].prefix
            else:
                return "--without-openssl"
        else:
            if activated:
                return "--with-ssl=" + self.spec["openssl"].prefix
            else:
                return "--without-ssl"

    def with_or_without_secure_transport(self, activated):
        if self.spec.satisfies("@7.65:"):
            if activated:
                return "--with-secure-transport"
            else:
                return "--without-secure-transport"
        else:
            if activated:
                return "--with-darwinssl"
            else:
                return "--without-darwinssl"


class NMakeBuilder(BuildEnvironment, NMakeBuilder):
    phases = ["install"]

    def nmake_args(self):
        args = []
        mode = "dll" if self.spec.satisfies("libs=shared") else "static"
        args.append("mode=%s" % mode)
        args.append("WITH_ZLIB=%s" % mode)
        args.append("ZLIB_PATH=%s" % self.spec["zlib-api"].prefix)
        if "+libssh" in self.spec:
            args.append("WITH_SSH=%s" % mode)
        if "+libssh2" in self.spec:
            args.append("WITH_SSH2=%s" % mode)
            args.append("SSH2_PATH=%s" % self.spec["libssh2"].prefix)
        if "+nghttp2" in self.spec:
            args.append("WITH_NGHTTP2=%s" % mode)
            args.append("NGHTTP2=%s" % self.spec["nghttp2"].prefix)
        if "tls=openssl" in self.spec:
            args.append("WITH_SSL=%s" % mode)
            args.append("SSL_PATH=%s" % self.spec["openssl"].prefix)
        elif "tls=mbedtls" in self.spec:
            args.append("WITH_MBEDTLS=%s" % mode)
            args.append("MBEDTLS_PATH=%s" % self.spec["mbedtls"].prefix)
        elif "tls=sspi" in self.spec:
            args.append("ENABLE_SSPI=%s" % mode)

        # The trailing path seperator is REQUIRED for cURL to install
        # otherwise cURLs build system will interpret the path as a file
        # and the install will fail with ambiguous errors
        inst_prefix = self.prefix + "\\"
        args.append(f"WITH_PREFIX={windows_sfn(inst_prefix)}")
        return args

    def install(self, pkg, spec, prefix):
        # Spack's env CC and CXX values will cause an error
        # if there is a path in the space, and escaping with
        # double quotes raises a syntax issues, instead
        # cURLs nmake will automatically invoke proper cl.exe if
        # no env value for CC, CXX is specified
        # Unset the value to allow for cURLs heuristics (derive via VCVARS)
        # to derive the proper compiler
        env = os.environ
        env["CC"] = ""
        env["CXX"] = ""
        winbuild_dir = os.path.join(self.stage.source_path, "winbuild")
        winbuild_dir = windows_sfn(winbuild_dir)
        with working_dir(winbuild_dir):
            nmake("/f", "Makefile.vc", *self.nmake_args(), ignore_quotes=True)
        with working_dir(os.path.join(self.stage.source_path, "builds")):
            install_dir = glob.glob("libcurl-**")[0]
            install_tree(install_dir, self.prefix)
        if spec.satisfies("libs=static"):
            # curl is named libcurl_a when static on Windows
            # Consumers look for just libcurl
            # make a symlink to make consumers happy
            libcurl_a = os.path.join(prefix.lib, "libcurl_a.lib")
            libcurl = os.path.join(self.prefix.lib, "libcurl.lib")
            # safeguard against future curl releases that do this for us
            if os.path.exists(libcurl_a) and not os.path.exists(libcurl):
                symlink(libcurl_a, libcurl)
