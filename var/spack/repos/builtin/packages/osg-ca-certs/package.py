# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OsgCaCerts(Package):
    """OSG Packaging of the IGTF CA Certs and OSG-specific CAs,
    in the OpenSSL 1.0.* format."""

    homepage = "http://repo.opensciencegrid.org/cadist"
    url = "https://github.com/opensciencegrid/osg-certificates/archive/v1.109.igtf.1.117/osg-certificates-1.109.igtf.1.117.tar.gz"

    _osg_base_url = "https://github.com/opensciencegrid/osg-certificates/archive/v{osg_version}.igtf.{igtf_version}/osg-certificates-{osg_version}.igtf.{igtf_version}.tar.gz"
    _igtf_base_url = "https://dist.eugridpma.info/distribution/igtf/{igtf_version}/igtf-policy-installation-bundle-{igtf_version}.tar.gz"
    _letsencrypt_base_url = "https://github.com/opensciencegrid/letsencrypt-certificates/archive/v{letsencrypt_version}/letsencrypt-certificates.tar.gz"

    maintainers("wdconinc")

    releases = [
        {
            "osg_version": "1.110",
            "igtf_version": "1.119",
            "osg_sha256": "025969d415bf27c1609699caf63d0d79540a01df500187195f2bd973fe69e00d",
            "igtf_sha256": "cc4db07a86fc27f0e0dfd15c797d1a0da7b5620f4b611dbb686543712b2f335a",
        },
        {
            "osg_version": "1.109",
            "igtf_version": "1.117",
            "osg_sha256": "41e12c05aedb4df729bf326318cc29b9b79eb097564fd68c6af2e1448ec74f75",
            "igtf_sha256": "130d4d95cd65d01d2db250ee24c539341e3adc899b7eff1beafef1ba4674807d",
        },
    ]

    for release in releases:
        _version = "{0}.igtf.{1}".format(release["osg_version"], release["igtf_version"])

        version(
            _version,
            url=_osg_base_url.format(
                osg_version=release["osg_version"], igtf_version=release["igtf_version"]
            ),
            sha256=release["osg_sha256"],
        )

        resource(
            name="igtf-{igtf_version}".format(igtf_version=release["igtf_version"]),
            url=_igtf_base_url.format(igtf_version=release["igtf_version"]),
            sha256=release["igtf_sha256"],
            when="@{0}".format(_version),
        )

    resource(
        name="letsencrypt",
        git="https://github.com/opensciencegrid/letsencrypt-certificates",
        branch="master",
        destination="letsencrypt-certificates-master",
    )

    depends_on("openssl")

    def setup_build_environment(self, env):
        env.set("OSG_CERTS_VERSION", self.version[:2])
        env.set("OUR_CERTS_VERSION", str(self.version[:2]) + "NEW")
        env.set("IGTF_CERTS_VERSION", self.version[3:])
        env.set("CADIST", join_path(self.stage.source_path, "certificates"))
        env.set("PKG_NAME", self.spec.name)

    def setup_run_environment(self, env):
        env.set("X509_CERT_DIR", join_path(self.prefix, "certificates"))

    def install(self, spec, prefix):
        copy_tree(
            "letsencrypt-certificates-master/letsencrypt-certificates", "letsencrypt-certificates"
        )
        Executable(join_path(self.stage.source_path, "build-certificates-dir.sh"))()
        install_tree("certificates", join_path(prefix, "certificates"))
