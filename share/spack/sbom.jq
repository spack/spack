{
  "spdxVersion": "SPDX-2.3",
  "dataLicense": "CC0-1.0",
  "SPDXID": "SPDXRef-DOCUMENT-zlib-1.3.1",
  "documentNamespace": "https://spack.io/sbom/unique-str",
  "creationInfo": {
    "created": "2025-12-11T23:24:43Z",
    "creators": [
      "Organization: Spack Project",
      "Tool: Spack"
    ]
  },
  "name": "zlib-1.3.1-hsvhdjxvsyzuejvpywwqnox6lswx2jsy",
  "packages": [
    {
      "SPDXID": "SPDXRef-PACKAGE-zlib-1.3.1",
      "name": "zlib",
      "versionInfo": "1.3.1",
      "supplier": "Organization: madler",
      "downloadLocation": "http://zlib.net/fossils/zlib-1.2.11.tar.gz",
      "filesAnalyzed": false,
      "licenseDeclared": "Zlib",
      "licenseConcluded": "NOASSERTION"
    },
    {
      "SPDXID": "SPDXRef-PACKAGE-apple-clang-17.0.0",
      "name": "apple-clang",
      "versionInfo": "1.3.1",
      "supplier": "Organization: madler",
      "downloadLocation": "NOASSERTION",
      "filesAnalyzed": false,
      "licenseDeclared": "NOASSERTION",
      "licenseConcluded": "NOASSERTION"
    },
    {
      "SPDXID": "SPDXRef-PACKAGE-compiler-wrapper-1.0",
      "name": "compiler-wrapper",
      "versionInfo": "1.3.1",
      "supplier": "Organization: madler",
      "downloadLocation": "file:////Users/shea9/spack-packages/repos/spack_repo/builtin/packages/compiler_wrapper/cc.sh",
      "filesAnalyzed": false,
      "licenseDeclared": "Apache-2.0 OR MIT",
      "licenseConcluded": "NOASSERTION"
    },
    {
      "SPDXID": "SPDXRef-PACKAGE-gmake-4.4.1",
      "name": "gmake",
      "versionInfo": "1.3.1",
      "supplier": "Organization: madler",
      "downloadLocation": "NOASSERTION",
      "filesAnalyzed": false,
      "licenseDeclared": "GPL-3.0-only",
      "licenseConcluded": "NOASSERTION"
    }
  ],
  "relationships": [
    {
      "spdxElementId": "SPDXRef-DOCUMENT-zlib-1.3.1",
      "relationshipType": "DESCRIBES",
      "relatedSpdxElement": "SPDXRef-PACKAGE-zlib-1.3.1"
    },
    {
      "spdxElementId": "SPDXRef-PACKAGE-zlib-1.3.1",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-PACKAGE-apple-clang-17.0.0"
    },
    {
      "spdxElementId": "SPDXRef-PACKAGE-zlib-1.3.1",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-PACKAGE-compiler-wrapper-1.0"
    },
    {
      "spdxElementId": "SPDXRef-PACKAGE-zlib-1.3.1",
      "relationshipType": "CONTAINS",
      "relatedSpdxElement": "SPDXRef-PACKAGE-gmake-4.4.1"
    }
  ]
}
