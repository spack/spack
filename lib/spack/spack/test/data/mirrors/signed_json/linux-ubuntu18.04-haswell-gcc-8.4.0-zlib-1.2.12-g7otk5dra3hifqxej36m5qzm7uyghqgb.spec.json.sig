-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

{
  "spec": {
    "_meta": {
      "version": 2
    },
    "nodes": [
      {
        "name": "zlib",
        "version": "1.2.12",
        "arch": {
          "platform": "linux",
          "platform_os": "ubuntu18.04",
          "target": {
            "name": "haswell",
            "vendor": "GenuineIntel",
            "features": [
              "aes",
              "avx",
              "avx2",
              "bmi1",
              "bmi2",
              "f16c",
              "fma",
              "mmx",
              "movbe",
              "pclmulqdq",
              "popcnt",
              "rdrand",
              "sse",
              "sse2",
              "sse4_1",
              "sse4_2",
              "ssse3"
            ],
            "generation": 0,
            "parents": [
              "ivybridge",
              "x86_64_v3"
            ]
          }
        },
        "compiler": {
          "name": "gcc",
          "version": "8.4.0"
        },
        "namespace": "builtin",
        "parameters": {
          "optimize": true,
          "patches": [
            "0d38234384870bfd34dfcb738a9083952656f0c766a0f5990b1893076b084b76"
          ],
          "pic": true,
          "shared": true,
          "cflags": [],
          "cppflags": [],
          "cxxflags": [],
          "fflags": [],
          "ldflags": [],
          "ldlibs": []
        },
        "patches": [
          "0d38234384870bfd34dfcb738a9083952656f0c766a0f5990b1893076b084b76"
        ],
        "package_hash": "bm7rut622h3yt5mpm4kvf7pmh7tnmueezgk5yquhr2orbmixwxuq====",
        "hash": "g7otk5dra3hifqxej36m5qzm7uyghqgb",
        "full_hash": "fx2fyri7bv3vpz2rhke6g3l3dwxda4t6",
        "build_hash": "g7otk5dra3hifqxej36m5qzm7uyghqgb"
      }
    ]
  },
  "binary_cache_checksum": {
    "hash_algorithm": "sha256",
    "hash": "5b9a180f14e0d04b17b1b0c2a26cf3beae448d77d1bda4279283ca4567d0be90"
  },
  "buildinfo": {
    "relative_prefix": "linux-ubuntu18.04-haswell/gcc-8.4.0/zlib-1.2.12-g7otk5dra3hifqxej36m5qzm7uyghqgb",
    "relative_rpaths": false
  }
}
-----BEGIN PGP SIGNATURE-----

iQEzBAEBCgAdFiEEz8AGj4zHZe4OaI2OQ0Tg92UAr50FAmJ5lD4ACgkQQ0Tg92UA
r52LEggAl/wXlOlHDnjWvqBlqAn3gaJEZ5PDVPczk6k0w+SNfDGrHfWJnL2c23Oq
CssbHylSgAFvaPT1frbiLfZj6L4j4Ym1qsxIlGNsVfW7Pbc4yNF0flqYMdWKXbgY
2sQoPegIKK7EBtpjDf0+VRYfJTMqjsSgjT/o+nTkg9oAnvU23EqXI5uiY84Z5z6l
CKLBm0GWg7MzI0u8NdiQMVNYVatvvZ8EQpblEUQ7jD4Bo0yoSr33Qdq8uvu4ZdlW
bvbIgeY3pTPF13g9uNznHLxW4j9BWQnOtHFI5UKQnYRner504Yoz9k+YxhwuDlaY
TrOxvHe9hG1ox1AP4tqQc+HsNpm5Kg==
=gi2R
-----END PGP SIGNATURE-----
