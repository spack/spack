# Spack v1.0.0 Release notes

## Package API
- Added `PackageBase.default_buildsystem`. 
  Deprecated the implicit attributes `PackageBase.legacy_buildsystem`.
  Bumped the package API to v2.2

- Added `CompilerError` and `SpackError` to the list of names exported in `spack.package`.
  Bumped the package API to v2.1
