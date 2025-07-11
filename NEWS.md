# Spack v1.0.0 Release notes

## Package API
- Added:
  - `PackageBase.default_buildsystem`
  - `Builder.package_methods`
  - `Builder.package_attributes`
  - `Builder.package_long_methods`

  Deprecated the implicit attributes:
  - `PackageBase.legacy_buildsystem`
  - `Builder.legacy_methods`
  - `Builder.legacy_attributes`
  - `Builder.legacy_long_methods`

  Bumped the package API to v2.2

- Added `CompilerError` and `SpackError` to the list of names exported in `spack.package`.
  Bumped the package API to v2.1
