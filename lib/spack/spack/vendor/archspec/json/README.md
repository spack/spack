[![](https://github.com/archspec/archspec-json/workflows/JSON%20Validation/badge.svg)](https://github.com/archspec/archspec-json/actions)

# Archspec-json

The [archspec-json](https://github.com/archspec/archspec-json) repository is part of the
[Archspec](https://github.com/archspec) project. It contains data on various architectural
aspects of a platform stored in JSON format and is meant to be used as a base to develop
language specific APIs.

Currently the repository contains the following JSON files:
```console
cpu/
├── cpuid.json                     # Contains information on CPUID calls to retrieve vendor and features on x86_64
├── cpuid_schema.json              # Schema for the file above
├── microarchitectures.json        # Contains information on CPU microarchitectures
└── microarchitectures_schema.json # Schema for the file above
gpu/
├── microarchitectures.json        # Contains information on GPU microarchitectures
└── microarchitectures_schema.json # Schema for the file above
```

## GPU microarchitectures

`gpu/microarchitectures.json` encodes binary compatibility between GPU targets as a graph,
in the same form as the CPU file: each node lists its direct parents in `from`, and a device at
a node runs binaries built for any of its ancestors. Hosts are expected to map to the most
specific node for their silicon (for example a compute capability 10.0 device is `10.0a`).

Node names are the identifiers compilers use:

* NVIDIA: the compute capability `X.Y`, plus `X.Yf` (family-specific, CUDA 12.9+) and `X.Ya`
  (architecture-specific) targets.
* AMD: the LLVM processor name `gfxNNN`, plus `gfxNNN:xnack-` / `gfxNNN:xnack+` target IDs
  where Spack exposes them.

Edges follow these rules:

* NVIDIA base targets chain in minor-version order within a major version (`8.0 <- 8.6 <- 8.7`),
  since a cubin built for `X.y` runs on `X.z` for `z >= y`. The first of each major hangs off
  the `nvidia` root.
* `X.Yf` has parents `X.Y` and the `f` target of every earlier member of its family, per the
  family table in the CUDA programming guide (`100f` runs on 10.0, 10.3, 10.7; `120f` on 12.0,
  12.1).
* `X.Ya` has `X.Yf` as its parent (or `X.Y` where no `f` target exists) and runs only on `X.Y`.
* Compute capability 10.1 (CUDA 12.8 and 12.9 only, renamed 11.0 in CUDA 13) is an isolated
  chain off the root with no edges to 10.0 or 11.0.
* Every AMD `gfxNNN` hangs off the `amd` root. `gfxNNN:xnack-` and `gfxNNN:xnack+` have `gfxNNN`
  as parent: a device in either mode runs code objects built without an xnack setting, but the
  two modes do not run each other's code objects.

`compilers` entries follow the CPU layout. `versions` is the range of compiler releases that can
emit code for the target (ROCm release numbers for `hipcc`, CUDA toolkit for `nvcc`, upstream
LLVM for `clang`), not the range in which the vendor supports the product.


## License

Archspec is distributed under the terms of both the MIT license and the
Apache License (Version 2.0). Users may choose either license, at their
option.

All new contributions must be made under both the MIT and Apache-2.0
licenses.

See [LICENSE-MIT](https://github.com/archspec/archspec-json/blob/master/LICENSE-MIT),
[LICENSE-APACHE](https://github.com/archspec/archspec-json/blob/master/LICENSE-APACHE),
[COPYRIGHT](https://github.com/archspec/archspec-json/blob/master/COPYRIGHT), and
[NOTICE](https://github.com/archspec/archspec-json/blob/master/NOTICE) for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811653
