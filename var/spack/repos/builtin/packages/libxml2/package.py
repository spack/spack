# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.filesystem as fs
import llnl.util.tty as tty

from spack.package import *


class Libxml2(AutotoolsPackage):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
    project (but usable outside of the Gnome platform), it is free
    software available under the MIT License."""

    homepage = "http://xmlsoft.org"
    url = "https://download.gnome.org/sources/libxml2/2.9/libxml2-2.9.13.tar.xz"
    list_url = "https://gitlab.gnome.org/GNOME/libxml2/-/releases"

    def url_for_version(self, version):
        if version >= Version("2.9.13"):
            url = "https://download.gnome.org/sources/libxml2/{0}/libxml2-{1}.tar.xz"
            return url.format(version.up_to(2), version)
        return "http://xmlsoft.org/sources/libxml2-{0}.tar.gz".format(version)

    version("2.10.3", sha256="5d2cc3d78bec3dbe212a9d7fa629ada25a7da928af432c93060ff5c17ee28a9c")
    version("2.10.2", sha256="d240abe6da9c65cb1900dd9bf3a3501ccf88b3c2a1cb98317d03f272dda5b265")
    version("2.10.1", sha256="21a9e13cc7c4717a6c36268d0924f92c3f67a1ece6b7ff9d588958a6db9fb9d8")
    version("2.9.14", sha256="60d74a257d1ccec0475e749cba2f21559e48139efba6ff28224357c7c798dfee")
    version("2.9.13", sha256="276130602d12fe484ecc03447ee5e759d0465558fbc9d6bd144e3745306ebf0e")
    version("2.9.12", sha256="c8d6681e38c56f172892c85ddc0852e1fd4b53b4209e7f4ebf17f7e2eae71d92")
    version("2.9.11", sha256="886f696d5d5b45d780b2880645edf9e0c62a4fd6841b853e824ada4e02b4d331")
    version("2.9.10", sha256="aafee193ffb8fe0c82d4afef6ef91972cbaf5feea100edc2f262750611b4be1f")
    version("2.9.9", sha256="94fb70890143e3c6549f265cee93ec064c80a84c42ad0f23e85ee1fd6540a871")
    version("2.9.8", sha256="0b74e51595654f958148759cfef0993114ddccccbb6f31aee018f3558e8e2732")
    version("2.9.4", sha256="ffb911191e509b966deb55de705387f14156e1a56b21824357cdf0053233633c")
    version("2.9.2", sha256="5178c30b151d044aefb1b08bf54c3003a0ac55c59c866763997529d60770d5bc")
    version("2.7.8", sha256="cda23bc9ebd26474ca8f3d67e7d1c4a1f1e7106364b690d822e009fdc3c417ec")

    variant("python", default=False, description="Enable Python support")

    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("iconv")
    depends_on("zlib")
    depends_on("xz")

    # avoid cycle dependency for concretizer
    with when("+python"):
        depends_on("python+shared~libxml2")
        # A note about python versions: libxml 2.10.1 (and presumably earlier) has
        # a bug in its configure script that fails to properly parse python
        # version strings with more than one character for the minor version.
        depends_on("python@:3.9", when="@:2.10.1")
    extends(
        "python",
        when="+python",
        ignore=r"(bin.*$)|(include.*$)|(share.*$)|(lib/libxml2.*$)|"
        "(lib/xml2.*$)|(lib/cmake.*$)",
    )

    # XML Conformance Test Suites
    # See https://www.w3.org/XML/Test/ for information
    resource(
        name="xmlts",
        url="https://www.w3.org/XML/Test/xmlts20080827.tar.gz",
        sha256="96151685cec997e1f9f3387e3626d61e6284d4d6e66e0e440c209286c03e9cc7",
    )

    patch("nvhpc-elfgcchack.patch", when="@:2.9 %nvhpc")

    # Use NAN/INFINITY if available to avoid SIGFPE
    # See https://gitlab.gnome.org/GNOME/libxml2/-/merge_requests/186
    patch(
        "https://gitlab.gnome.org/GNOME/libxml2/-/commit/c9925454fd384a17c8c03d358c6778a552e9287b.patch",
        sha256="3e06d42596b105839648070a5921157fe284b932289ffdbfa304ddc3457e5637",
        when="@2.9.11:2.9.14",
    )

    @property
    def command(self):
        return Executable(self.prefix.bin.join("xml2-config"))

    @property
    def headers(self):
        include_dir = self.spec.prefix.include.libxml2
        hl = find_all_headers(include_dir)
        hl.directories = [include_dir, self.spec.prefix.include]
        return hl

    def configure_args(self):
        spec = self.spec

        args = [
            "--with-lzma={0}".format(spec["xz"].prefix),
            "--with-iconv={0}".format(spec["iconv"].prefix),
        ]

        if "+python" in spec:
            args.extend(
                [
                    "--with-python={0}".format(spec["python"].home),
                    "--with-python-install-dir={0}".format(python_platlib),
                ]
            )
        else:
            args.append("--without-python")

        return args

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file(
                "-pedantic -Wall -Wextra -Wshadow -Wpointer-arith "
                "-Wcast-align -Wwrite-strings -Waggregate-return "
                "-Wstrict-prototypes -Wmissing-prototypes "
                "-Wnested-externs -Winline -Wredundant-decls",
                "-Wall",
                "configure",
            )
            filter_file("-Wno-long-long -Wno-format-extra-args", "", "configure")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if "+python" in self.spec:
            with working_dir("spack-test", create=True):
                python("-c", "import libxml2")

    def test(self):
        """Perform smoke tests on the installed package"""
        # Start with what we already have post-install
        tty.msg("test: Performing simple import test")
        self.import_module_test()

        data_dir = self.test_suite.current_test_data_dir

        # Now run defined tests based on expected executables
        dtd_path = data_dir.join("info.dtd")
        test_filename = "test.xml"
        exec_checks = {
            "xml2-config": [("--version", [str(self.spec.version)], 0)],
            "xmllint": [
                (["--auto", "-o", test_filename], [], 0),
                (
                    ["--postvalid", test_filename],
                    ["validity error", "no DTD found", "does not validate"],
                    3,
                ),
                (
                    ["--dtdvalid", dtd_path, test_filename],
                    ["validity error", "does not follow the DTD"],
                    3,
                ),
                (["--dtdvalid", dtd_path, data_dir.join("info.xml")], [], 0),
            ],
            "xmlcatalog": [("--create", ["<catalog xmlns", 'catalog"/>'], 0)],
        }
        for exe in exec_checks:
            for options, expected, status in exec_checks[exe]:
                self.run_test(exe, options, expected, status)

        # Perform some cleanup
        fs.force_remove(test_filename)
