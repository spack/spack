## Spack v1.0.0
Deprecated the implicit attributes:
- `PackageBase.legacy_buildsystem`
- `Builder.legacy_methods`
- `Builder.legacy_attributes`
- `Builder.legacy_long_methods`

## Package API v2.2
Added to `spack.package`:
- `PackageBase.default_buildsystem`
- `Builder.package_methods`
- `Builder.package_attributes`
- `Builder.package_long_methods`
- `set_env` context manager
- `BuilderWithDefaults` base class
- `apply_macos_rpath_fixups` and `execute_install_time_tests` helper functions
- `GenericBuilder` and `Package` classes
- `get_cmake_prefix_path`
- `microarchitecture_flags_from_target`
- `microarchitecture_flags`
- `shared_library_suffix`
- `static_library_suffix`

## Package API v2.1
Added to `spack.package`:
- `CompilerError`
- `SpackError`
